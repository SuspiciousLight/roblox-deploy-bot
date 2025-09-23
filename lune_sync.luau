local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- Parse flags: --place-file <path> --data-dir <path>
local placeFile: string? = nil
local dataDir: string? = nil

local function parseArgs(...)
	local argv = {...}
	local i = 1
	while i <= #argv do
		local a = argv[i]
		if a == "--place-file" then
			placeFile = argv[i + 1]
			i += 1
		elseif a == "--data-dir" then
			dataDir = argv[i + 1]
			i += 1
		end
		i += 1
	end
	assert(placeFile and placeFile ~= "", "--place-file is required")
	assert(dataDir and dataDir ~= "", "--data-dir is required")
end

local function readTextFile(filePath: string): string?
	local ok, content = pcall(function()
		return readfile(filePath)
	end)
	if ok then
		return content
	else
		return nil
	end
end

local function ensureFolder(parent: Instance, name: string): Instance
	local f = parent:FindFirstChild(name)
	if not f then
		f = Instance.new("Folder")
		f.Name = name
		f.Parent = parent
	end
	return f
end

local function pathJoin(a: string, b: string): string
	if a:sub(-1):match("[\\/]") then
		return a .. b
	else
		return a .. "/" .. b
	end
end

local function getBaseName(filePath: string): string
	return filePath:match("([^/\\]+)$") or filePath
end

local function isDirectory(path: string): boolean
	local ok, entries = pcall(function()
		return listfiles(path)
	end)
	return ok and type(entries) == "table"
end

local function ensureModuleScript(parent: Instance, name: string): ModuleScript
	local child = parent:FindFirstChild(name)
	if not child or not child:IsA("ModuleScript") then
		if child then child:Destroy() end
		child = Instance.new("ModuleScript")
		child.Name = name
		child.Parent = parent
	end
	return child :: ModuleScript
end

local function syncDirectory(sourceDir: string, parentInstance: Instance)
	local entries = listfiles(sourceDir)
	for _, entryPath in ipairs(entries) do
		local base = getBaseName(entryPath)
		if isDirectory(entryPath) then
			local folder = ensureFolder(parentInstance, base)
			syncDirectory(entryPath, folder)
		else
			if base:match("%.lua$") or base:match("%.luau$") then
				local moduleName = (base:gsub("%.lua[u]?$", ""))
				local source = readTextFile(entryPath)
				if source then
					local moduleScript = ensureModuleScript(parentInstance, moduleName)
					moduleScript.Source = source
					print("Synced module:", moduleName)
				else
					warn("Failed to read:", entryPath)
				end
			elseif base:match("%.json$") then
				local moduleName = (base:gsub("%.json$", ""))
				local jsonContent = readTextFile(entryPath)
				if jsonContent then
					local moduleScript = ensureModuleScript(parentInstance, moduleName)
					local luaSource = "return " .. jsonContent
					moduleScript.Source = luaSource
					print("Synced JSON module:", moduleName)
				else
					warn("Failed to read JSON:", entryPath)
				end
			end
		end
	end
end

local function syncModuleScripts()
	local modulesRoot = ensureFolder(ReplicatedStorage, "Modules")
	local dataFolder = ensureFolder(modulesRoot, "Data")
	syncDirectory(dataDir :: string, dataFolder)
end

print("Starting data sync...")
parseArgs()
print("Place file:", placeFile)
print("Data directory:", dataDir)

local okLoad, errLoad = pcall(function()
	game:Load(placeFile :: string)
end)
if not okLoad then
	error("Failed to load place file: " .. tostring(errLoad))
end

syncModuleScripts()

local okSave, errSave = pcall(function()
	game:Save(placeFile :: string)
end)
if not okSave then
	error("Failed to save place file: " .. tostring(errSave))
end

print("Data sync completed successfully!")
