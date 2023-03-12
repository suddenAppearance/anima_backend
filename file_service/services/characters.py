import asyncio
import logging
import os
from contextlib import contextmanager
from datetime import datetime
from urllib.parse import quote
from uuid import UUID

from fastapi import HTTPException, Depends
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
import bpy
from starlette.responses import StreamingResponse

from api.api_v1.deps import get_session
from schemas.blender import Vector3D
from schemas.files import FileMetaTypeEnum, FileMetaRetrieveSchema, FileInfoRetrieveSchema
from services.base import AnimationServiceMixin, FileMetaServiceMixin, FileServiceMixin


class AnimationService(AnimationServiceMixin, FileMetaServiceMixin, FileServiceMixin):
    def __init__(self, request: Request, session: AsyncSession = Depends(get_session)):
        super().__init__(request=request, session=session)
        self.lock = asyncio.Lock()

    @staticmethod
    def _generate_unique_filename(file: FileInfoRetrieveSchema):
        return f"/tmp/{file.id}-{datetime.now()}-{file.initial_filename}"

    @staticmethod
    def _blender_clear():
        bpy.ops.wm.read_homefile(use_empty=True)

    @contextmanager
    def blender_lock(self):
        try:
            self._blender_clear()
            yield self.lock
        finally:
            self._blender_clear()

    @staticmethod
    def _import_fbx(filepath):
        bpy.ops.import_scene.fbx(filepath=filepath)

    @staticmethod
    def _get_dimensions():
        dims = bpy.context.object.dimensions
        return Vector3D(x=dims.x, y=dims.y, z=dims.z)

    def _blender_import(self, filepath):
        self._import_fbx(filepath)
        return bpy.context.object

    @staticmethod
    def deselect_all():
        bpy.ops.object.select_all(action="DESELECT")

    @staticmethod
    def select(obj):
        obj.select_set(True)

    @staticmethod
    def deselect(obj):
        obj.select_set(False)

    @staticmethod
    def set_active(obj):
        bpy.context.view_layer.objects.active = obj

    @staticmethod
    def link_animation_data():
        bpy.ops.object.make_links_data(type="ANIMATION")

    @staticmethod
    def make_single_user_animation():
        bpy.ops.object.make_single_user(animation=True, obdata_animation=True)

    @classmethod
    def get_child_names(cls, obj):
        names = set()
        for child in obj.children:
            names.add(child.name)
            if child.children:
                cls.get_child_names(child)

        return names

    @classmethod
    def delete_hierarchy(cls, obj):
        names = cls.get_child_names(obj)
        names.add(obj.name)
        print(names)
        [cls.select(bpy.data.objects[n]) for n in names]
        bpy.ops.object.delete()

    @classmethod
    def _animate(cls, obj1, obj2):
        cls.deselect_all()
        cls.set_active(obj2)
        cls.select(obj1)
        cls.link_animation_data()
        cls.make_single_user_animation()

    @classmethod
    def export(cls, filepath):
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            object_types={"ARMATURE", "MESH", "OTHER"},
            bake_anim=True,
            bake_anim_step=1,
            bake_anim_use_all_bones=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            bake_anim_simplify_factor=1,
        )

    async def _blender_link_animation(self, model: FileMetaRetrieveSchema, animation: FileMetaRetrieveSchema):
        model_file = self.file_service.download_file(model.file)
        model_path = self._generate_unique_filename(file=model.file)

        animation_file = self.file_service.download_file(animation.file)
        animation_path = self._generate_unique_filename(file=animation.file)
        with open(model_path, "wb") as f:
            f.write(model_file.read())
        with open(animation_path, "wb") as f:
            f.write(animation_file.read())

        with self.blender_lock():
            obj1 = self._blender_import(model_path)
            obj2 = self._blender_import(animation_path)
            self._animate(obj1, obj2)
            self.deselect_all()
            self.delete_hierarchy(obj2)
            self.export(animation_path)

        os.remove(model_path)

        stream = open(animation_path, "rb")

        return stream

    async def animate(self, model_id: UUID, animation_model_id: UUID):
        model = await self.file_meta_service.get_full_file(model_id)
        if not model:
            raise HTTPException(status_code=404)
        if model.type != FileMetaTypeEnum.CHARACTER:
            raise HTTPException(status_code=400)

        animation = await self.file_meta_service.get_full_file(animation_model_id)
        if not animation:
            raise HTTPException(status_code=404)
        if animation.type != FileMetaTypeEnum.ANIMATION:
            raise HTTPException(status_code=400)

        stream = await self._blender_link_animation(model, animation)

        response = StreamingResponse(stream)
        response.raw_headers.append(
            (
                b"content-disposition",
                f"attachment; filename*=utf-8''{quote(animation.file.initial_filename)}".encode("latin-1"),
            )
        )

        return response
