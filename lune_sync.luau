local HttpService = game:GetService("HttpService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local args = {...}
local placeFile = args[1] or error("Place file path required")
local dataDir = args[2] or error("Data directory path required")

local function loadJsonFile(filePath)
    local success, content = pcall(function()
        return readfile(filePath)
    end)
    
    if not success then
        warn("Failed to read file:", filePath)
        return nil
    end
    
    local success, data = pcall(function()
        return HttpService:JSONDecode(content)
    end)
    
    if not success then
        warn("Failed to parse JSON:", filePath)
        return nil
    end
    
    return data
end

local function syncDataFiles()
    local dataFilesFolder = ReplicatedStorage:FindFirstChild("DataFiles")
    if not dataFilesFolder then
        dataFilesFolder = Instance.new("Folder")
        dataFilesFolder.Name = "DataFiles"
        dataFilesFolder.Parent = ReplicatedStorage
    end
    
    local files = listfiles(dataDir)
    
    for _, filePath in ipairs(files) do
        if filePath:match("%.json$") then
            local fileName = filePath:match("([^/\\]+)$")
            local data = loadJsonFile(filePath)
            
            if data then
                local stringValue = dataFilesFolder:FindFirstChild(fileName)
                if not stringValue then
                    stringValue = Instance.new("StringValue")
                    stringValue.Name = fileName
                    stringValue.Parent = dataFilesFolder
                end
                
                stringValue.Value = HttpService:JSONEncode(data)
                print("Synced data file:", fileName)
            end
        end
    end
end

print("Starting data sync...")
print("Place file:", placeFile)
print("Data directory:", dataDir)

local success, err = pcall(function()
    game:Load(placeFile)
end)

if not success then
    error("Failed to load place file: " .. tostring(err))
end

syncDataFiles()

local success, err = pcall(function()
    game:Save(placeFile)
end)

if not success then
    error("Failed to save place file: " .. tostring(err))
end

print("Data sync completed successfully!")
