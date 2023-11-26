fn convertToPhysicalMaterialAndReconnectMaps obj =
(
    if obj.material != undefined and classOf obj.material != PhysicalMaterial then
    (
        -- Create a new physical material
        local physMat = PhysicalMaterial()
        local oldMat = obj.material

        -- Example: Reconnect diffuse map (base color)
        -- Adjust this based on your specific needs and the structure of your original materials
        try
        (
            if oldMat.diffuseMap != undefined then
            (
                physMat.base_color_map = oldMat.diffuseMap
                physMat.base_color_map_enabled = true
            )
        ) catch ()
        
        -- Apply the new physical material to the object
        obj.material = physMat
    )
)


fn convertMaxToGLB path exportPath =
(
    for file in getFiles (path + "\\*.max") do
    (
        loadMaxFile file quiet:true

        -- Apply changes to each object in the scene
        for obj in objects do
        (
            convertToPhysicalMaterialAndReconnectMaps obj
        )

        exportFile (exportPath + "\\" + (getFilenameFile file) + ".glb") #noPrompt using:GLTFExporter
    )

    for dir in getDirectories (path + "\\*") do
    (
        convertMaxToGLB dir exportPath
    )
)

-- Usage
convertMaxToGLB "D:\\download 3d file\\Evermotion – Archmodels Vol.244\\Vray" "D:\\download 3d file\\Evermotion – Archmodels Vol.244\\Vray"
