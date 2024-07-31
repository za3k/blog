---
author: admin
categories:
- Technical
date: 2015-10-18 18:27:48-07:00
has-comments: true
markup: markdown
source: wordpress
tags:
- computercraft
- hacks
- minecraft
title: Controlling a computercraft turtle remotely
updated: 2015-11-29 23:04:07-07:00
wordpress_id: 313
wordpress_slug: controlling-a-computercraft-turtle-remotely
---
[![alt:Screen Shot 2015-10-18 at 7.16.59 PM](https://blog.za3k.com/wp-content/uploads/2015/10/Screen-Shot-2015-10-18-at-7.16.59-PM-1024x582.png)](https://blog.za3k.com/wp-content/uploads/2015/10/Screen-Shot-2015-10-18-at-7.16.59-PM.png)[![alt:Screen Shot 2015-10-18 at 7.17.30 PM](https://blog.za3k.com/wp-content/uploads/2015/10/Screen-Shot-2015-10-18-at-7.17.30-PM-300x197.png)](https://blog.za3k.com/wp-content/uploads/2015/10/Screen-Shot-2015-10-18-at-7.17.30-PM.png)

1.  Install Redis: [https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis)
2.  Install [Webdis  
    ](https://github.com/nicolasff/webdis)
3.  Start a minecraft server with computercraft. You will need to have the http API enabled, which is the default.
4.  Put down a turtle I recommend a turtle with a crafting square and a pickaxe. I also recommend giving it a label. If you’re not trying the [turtle replication challenge](http://www.computercraft.info/forums2/index.php?/topic/4462-competition/), either disable fuel or get a fair bit of starting fuel. Write down the computer’s id.
5.  Put down a chunk loader, if you’re in a modpack that has them, or DON’T log out. Computers and turtles can’t operate unless the chunks are loaded. If you’re putting down a chunkloader, I surrounded them with bedrock for foolproofing.
6.  Open the turtle and download the following script, changing “redis.example.com” to your own redis instance: pastebin get 8FjggG9w startup  
    After you have the script saved as ‘startup’, run it or reboot the computer, and it should start listening for instructions.
    
    ```
    redis = "http://redis.example.com" 
    queue = "sshbot" .. os.getComputerID()
    return_queue = queue .. "_return"
    print("Remote webdis queues on icyego: " .. queue .. " and " .. return_queue)
    print("Receiving remote commands.")
    
    function exec(str)
      print("Running: " .. str)
      f = fs.open("tmp", "w")
      f.write(str)
      f.close()
      p = loadfile("tmp")
     status, err = pcall(function () p = loadfile("tmp"); return p() end)
      if status then
        status, ret = pcall(function() return textutils.serialize(err) end)
        if status then
          result = ret
        else
          result = ""
        end
      else
        result = "Error: " .. err
      end
      print(result)
      return result
    end
    
    print("Now receiving remote commands.")
    while true do
      handle = http.get(redis .. "/BRPOP/" .. queue .. "/5.txt")
      if (handle and handle.getResponseCode() == 200) then 
        str = handle.readAll()
        handle.close()
        str = string.sub(str, string.len(queue) + 1)
        result = exec(str)
        if string.find(result, "Error: ") then
          result2 = exec("return " .. str)
          if string.find(result2, "Error: ") then a=0 else result=result2 end
        end
        http.post(redis, "LPUSH/" .. return_queue .. "/" .. result)
      end
    end
    ```
    
7.  On your local machine, save the following, again replacing “redis.example.com”:
    
    ```
    #!/bin/bash
    function send() {
      curl -s -X POST -d "LPUSH/sshbot${1}/${2}" "http://redis.example.com" >/dev/null
    
    }
    
    function get() {
      curl -s -X GET "http://redis.example.com/BRPOP/sshbot${1}_return/20.json" | jq .BRPOP[1]
    }
    
    if [ $# -ne 1 ]; then
      echo "Usage: rlwrap ./sshbot <COMPUTER_ID>"
      exit 1
    fi
    ID=$1
    
    while read LINE; do
      send ${ID} "$LINE"
      get ${ID}
    done
    ```
    
8.  Run: rlwrap ./sshbot <ID>, where <ID> is the turtle’s ID. You should be able to send commands to the computer now.
