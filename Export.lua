function LuaExportStart()
    package.path = package.path .. ";.\\LuaSocket\\?.lua"
    package.cpath = package.cpath .. ";.\\LuaSocket\\?.dll"
    socket = require("socket")
    host = host or "localhost"
    port = port or 9595
    c = socket.try(socket.connect(host, port))
    c:setoption("tcp-nodelay", true)
end

function LuaExportStop()
    socket.try(c:send("quit"))
    c:close()
end

function LuaExportActivityNextEvent(t)
    local tNext = t
    local worldObjects = LoGetWorldObjects()
    local messageData = {}

    for _, v in ipairs(worldObjects) do
        local group = v.GroupName or "No Group"
        local name = v.Name
        local coalition = v.Coalition
        local lat = v.LatLongAlt.Lat
        local long = v.LatLongAlt.Long
        local alt = v.LatLongAlt.Alt
        local data = string.format(
            "{'name':'%s','group':'%s','coalition':'%s','latitude':'%s','longitude':'%s','altitude':'%s'}", name, group,
            coalition, lat, long, alt)
        table.insert(messageData, data)
    end

    local message = "[" .. table.concat(messageData, ",") .. "]"
    local messageSize = #message
    local header = string.format("%8d", messageSize)
    socket.try(c:send(header .. message))

    tNext = tNext + 1
    return tNext
end
