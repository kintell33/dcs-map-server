function LuaExportStart()
    package.path  = package.path..";.\\LuaSocket\\?.lua"
    package.cpath = package.cpath..";.\\LuaSocket\\?.dll"
    socket = require("socket")
    host = host or "localhost"
    port = port or 9595
    c = socket.try(socket.connect(host, port))
    c:setoption("tcp-nodelay",true)
end

function LuaExportStop()
    socket.try(c:send("quit"))
    c:close()
    
end

function LuaExportActivityNextEvent(t)
	local tNext = t

	local o = LoGetWorldObjects()
    
    local messageData = "["

    for k,v in pairs(o) do
        if v.GroupName ~= nil then
            messageData = messageData .. "{'name':'" .. v.Name ..  "','group':'" .. v.GroupName .. "','coalition':'" .. v.Coalition .. "','latitude':'" .. v.LatLongAlt.Lat .. "','longitude':'" .. v.LatLongAlt.Long .. "','altitude':'" .. v.LatLongAlt.Alt .. "'}"
            messageData = messageData .. ","
        else
            messageData = messageData .. "{'name':'" .. v.Name ..  "','group':'No Group','coalition':'" .. v.Coalition .. "','latitude':'" .. v.LatLongAlt.Lat .. "','longitude':'" .. v.LatLongAlt.Long .. "','altitude':'" .. v.LatLongAlt.Alt .. "'}"
            messageData = messageData .. ","
        end
    end
    
    messageData = messageData .. "]"
    local messageSize = #messageData
    local header = string.format("%8d", messageSize)
    socket.try(c:send(header .. messageData))

	tNext = tNext + 1

	return tNext
end