# -*- coding: utf-8 -*-

import bpy

from . import properties
from . import operators
from . import panels

classes = (
    panels.prop_bone.MMDBonePanel,
    panels.prop_bone.MMDBoneATPanel,
    panels.prop_camera.MMDCameraPanel,
    panels.prop_material.MMDMaterialPanel,
    panels.prop_material.MMDTexturePanel,
    panels.prop_object.MMDModelObjectPanel,
    panels.prop_object.MMDRigidPanel,
    panels.prop_object.MMDJointPanel,
    panels.tool.MMDToolsObjectPanel,
    panels.tool.MMDMorphToolsPanel,
    panels.tool.MMDRigidbodySelectorPanel,
    panels.tool.MMDJointSelectorPanel,
    panels.tool.MMDDisplayItemsPanel,
    #panels.tool.UL_BoneMorphOffsets,
    #panels.tool.UL_joints,
    #panels.tool.UL_MaterialMorphOffsets,
    #panels.tool.UL_Morphs,
    #panels.tool.UL_ObjectsMixIn,
    #panels.tool.UL_rigidbodies,
    panels.view_prop.MMDModelObjectDisplayPanel,
    panels.view_prop.MMDViewPanel,
    operators.animation.SetFrameRange,
    operators.camera.ConvertToMMDCamera,
    operators.display_item.AddDisplayItem,
    operators.display_item.AddDisplayItemFrame,
    operators.display_item.MoveDownDisplayItem,
    operators.display_item.MoveDownDisplayItemFrame,
    operators.display_item.MoveUpDisplayItem,
    operators.display_item.MoveUpDisplayItemFrame,
    operators.display_item.RemoveDisplayItem,
    operators.display_item.RemoveDisplayItemFrame,
    operators.display_item.SelectCurrentDisplayItem,
    operators.fileio.ExportPmx,
    operators.fileio.ImportPmx,
    operators.fileio.ImportVmd,
    operators.fileio.ImportVmdToMMDModel,
    operators.material.ConvertMaterialsForCycles,
    operators.material.OpenSphereTextureSlot,
    operators.material.OpenTexture,
    operators.material.RemoveSphereTexture,
    operators.material.RemoveTexture,
    operators.misc.SeparateByMaterials,
    operators.model.ApplyAdditionalTransformConstraints,
    operators.model.BuildRig,
    operators.model.CleanRiggingObjects,
    operators.model.CreateMMDModelRoot,
    operators.morph.AddBoneMorph,
    operators.morph.AddBoneMorphOffset,
    operators.morph.AddMaterialMorph,
    operators.morph.AddMaterialOffset,
    operators.morph.AddVertexMorph,
    operators.morph.ApplyBoneOffset,
    operators.morph.ApplyMaterialOffset,
    operators.morph.AssignBoneToOffset,
    operators.morph.ClearTempMaterials,
    operators.morph.CreateWorkMaterial,
    operators.morph.EditBoneOffset,
    operators.morph.MoveDownMorph,
    operators.morph.MoveUpMorph,
    operators.morph.RemoveBoneMorphOffset,
    operators.morph.RemoveMaterialOffset,
    operators.morph.RemoveMorph,
    operators.morph.SelectRelatedBone,
    operators.rigid_body.RemoveJoint,
    operators.rigid_body.RemoveRigidBody,
    operators.view.ResetShading,
    operators.view.SetGLSLShading,
    operators.view.SetShadelessGLSLShading,
    properties.camera.MMDCamera,
    properties.bone.MMDBone,
    properties.material.MMDMaterial,
    properties.morph.BoneMorphData,
    properties.morph.BoneMorph,
    properties.morph.MaterialMorphData,
    properties.morph.MaterialMorph,
    properties.morph.VertexMorph,
    properties.rigid_body.MMDJoint,
    properties.rigid_body.MMDRigidBody,
    properties.root.MMDDisplayItem,
    properties.root.MMDDisplayItemFrame,
    properties.root.MMDRoot
)

bl_info= {
    "name": "mmd_tools",
    "author": "sugiany",
    "version": (0, 9, 9),
    "blender": (2, 80, 0),
    "location": "View3D > Tool > MMD Tools Panel",
    "description": "Utility tools for MMD model editing.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

# if "bpy" in locals():
#     import imp
#     if "import_pmx" in locals():
#         imp.reload(import_pmx)
#     if "export_pmx" in locals():
#         imp.reload(export_pmx)
#     if "import_vmd" in locals():
#         imp.reload(import_vmd)
#     if "mmd_camera" in locals():
#         imp.reload(mmd_camera)
#     if "utils" in locals():
#         imp.reload(utils)
#     if "cycles_converter" in locals():
#         imp.reload(cycles_converter)
#     if "auto_scene_setup" in locals():
#         imp.reload(auto_scene_setup)

def make_annotations(cls):
    """Converts class fields to annotations if running with Blender 2.8"""
    if bpy.app.version < (2, 80):
        return cls
    bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, tuple)}
    if bl_props:
        if '__annotations__' not in cls.__dict__:
            setattr(cls, '__annotations__', {})
        annotations = cls.__dict__['__annotations__']
        for k, v in bl_props.items():
            annotations[k] = v
            delattr(cls, k)
    return cls

def menu_func_import(self, context):
    self.layout.operator(operators.fileio.ImportPmx.bl_idname, text="MikuMikuDance Model (.pmd, .pmx)")
    self.layout.operator(operators.fileio.ImportVmd.bl_idname, text="MikuMikuDance Motion (.vmd)")

def menu_func_export(self, context):
    self.layout.operator(operators.fileio.ExportPmx.bl_idname, text="MikuMikuDance model (.pmx)")

def menu_func_armature(self, context):
    self.layout.operator(operators.model.CreateMMDModelRoot.bl_idname, text='Create MMD Model')


def register():
    for cls in classes:
        #make_annotations(cls) # what is this? Read the section on annotations above!
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_edit_armature_add.append(menu_func_armature)
    properties.register()

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    properties.unregister()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
