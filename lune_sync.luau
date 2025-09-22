-- Lune script to sync data files into the Roblox place
-- This script will be called by the Python bot

local HttpService = game:GetService("HttpService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Get command line arguments
local args = {...}
local placeFile = args[1] or error("Place file path required")
local dataDir = args[2] or error("Data directory path required")

-- Function to load JSON data
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

-- Function to sync data files
local function syncDataFiles()
    -- Ensure DataFiles folder exists
    local dataFilesFolder = ReplicatedStorage:FindFirstChild("DataFiles")
    if not dataFilesFolder then
        dataFilesFolder = Instance.new("Folder")
        dataFilesFolder.Name = "DataFiles"
        dataFilesFolder.Parent = ReplicatedStorage
    end
    
    -- Get all JSON files from the data directory
    local files = listfiles(dataDir)
    
    for _, filePath in ipairs(files) do
        if filePath:match("%.json$") then
            local fileName = filePath:match("([^/\\]+)$")
            local data = loadJsonFile(filePath)
            
            if data then
                -- Create or update StringValue with JSON data
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

-- Main execution
print("Starting data sync...")
print("Place file:", placeFile)
print("Data directory:", dataDir)

-- Load the place file
local success, err = pcall(function()
    game:Load(placeFile)
end)

if not success then
    error("Failed to load place file: " .. tostring(err))
end

-- Sync the data files
syncDataFiles()

-- Save the place file
local success, err = pcall(function()
    game:Save(placeFile)
end)

if not success then
    error("Failed to save place file: " .. tostring(err))
end

print("Data sync completed successfully!")
