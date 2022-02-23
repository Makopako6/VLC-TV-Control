----------------------------------------------------------------------------
-- channelwatch.lua v0.02
-- by Jason D. Ozubko - 2012,2018 (jdozubko@gmail.com)
----------------------------------------------------------------------------
-- This script file should be placed in the proper VLC playlist parser directory
-- For information about where this is, see:
--
--   http://wiki.videolan.org/Documentation:Play_HowTo/Building_Lua_Playlist_Scripts
--
-- This script processes and plays .channel files.  The format for these files
-- is simply the filenames of each video file, and the duration of the video,
-- for each video that you want to be in the programming for that channel.  
-- For example, "example.channel" might contain:
--
--     foo.mp4
--     10:21
--     bar.mov
--     43:17
--
-- Based on the day's date, the script will make a playlist of 30 hours of 
-- programming out of the video files in the .channel file.  The script will then
-- grab the current time, and set VLC to the proper position in the playlist and
-- in the video file, down to the second.
--
-- So for example, if the playlist loads and is in the middle of playing foo.mp4
-- and you then close VLC.  If you reopen VLC 2 minutes later, and reload the
-- same .channel file, the player will still be showing foo, but will be 2 
-- minutes further along in the show.
--
-- To create different channels, fill up .channel files with different video
-- files. To create different versions of the same channel put a different
-- 3 digit number on the first line of the .channel file. This digit acts as
-- a random seed that the script uses to build the daily schedule.
--
-- (modified from randomseek.lua by HostileFork, Sept 2011)

function probe()
	-- tell VLC we will handle anything ending in ".channel"
	return string.match(vlc.path, ".channel$")
end


function parse()
	-- if there is a playlist already, then clear it
	if vlc.playlist ~= nil then
		vlc.playlist.clear()
	end

	--STEP 1. LOAD IN ALL FILES IN THE .CHANNEL FILE	

	-- fulllist will contain a list of ALL the media files in the .channel
	fulllist = {}
	nfulllist = 0
	
	-- default channel number... used as a random seed when shuffling the playlist
	channum = 0

	-- set a flag to indicate that the first line doesn't need to be re-read
	skipfirst = true
	
	-- read a line from the .channel file
	line = vlc.readline()

	-- if the length is 3 digits or less...
	if string.len(line) <= 3 then
		-- try to use this as our channel number
		channum = tonumber(line)
		if channum == nil then
			channum = 0
		end
	
		-- we don't need to skip reading the first line
		skipfirst = false
	end 

	-- loop through the list...
	all_done = false
	while all_done == false do
	
		-- if firstread flag is not true, then go ahead and read
		if skipfirst == false then
			while true do
				-- read a line from the .channel file
				line = vlc.readline()

				-- make sure we don't have an empty line
				if line ~= "" then
					break
				end
			end
		end

		-- set the skipfirst flag... we're going to read from now on
		skipfirst = false

		-- if that line does not exist...
		if line == nil then
			break --we're done reading the file
		end
		
		-- get the first character of the line
		l = string.sub(line, 1, 1)
		
		-- if we have a number...
		if l == '0' or l == '1' or l == '2' or l == '3' or l == '4' or l == '5' or l == '6' or l == '7' or l == '8' or l == '9' then
		
			--the file somehow got misaligned... skip this entry
		
		-- we don't have a number
		else
		
			-- create an empty item for entry
			list_item = {}
				
			-- create a loop to find a valid entry item
			while true do
		
				-- use line as the file name
				list_item.path = "file:///"..line

				while true do
					-- read a line from the .channel file
					line = vlc.readline()

					-- make sure we don't have an empty line
					if line ~= "" then
						break
					end
				end
				
				-- if that line does not exist...
				if line == nil then
					all_done = true
					break --we're done reading the file
				end

				-- else, get the first character of the line
				l = string.sub(line, 1, 1)
				
				-- if we have a number...
				if l == '0' or l == '1' or l == '2' or l == '3' or l == '4' or l == '5' or l == '6' or l == '7' or l == '8' or l == '9' then
				
					-- debug
					--vlc.msg.info( "!!!FOUND!!! " .. list_item.path .. " > " .. line )
						
					-- read in the duration in seconds
					for _hour, _min, _sec in string.gmatch( line, "(%d*):(%d*):(%d*)" )
						do
							list_item.duration = (60 * 60 * _hour) + (60 * _min) + _sec
						end

					-- add the list item to the full list
					table.insert( fulllist, list_item )
					nfulllist = nfulllist + 1
					
					-- quit the entry loop
					break
				
				-- else we have a file name...
				else
				
					-- do nothing here, we'll loop back and consider this new file name as an entry
				
					-- debug
					--vlc.msg.info( "!!!FAILED AT!!! " .. line )
				
				end
				
			end -- entry loop
		
		end

	end -- all_done loop

	-- STEP 2. RANDOMIZE THE ORDER OF THE FULLLIST ARRAY

	-- get the current date
	cdate = os.date("*t")

	-- calculate the current second
	csec = (60 * 60 * cdate.hour) + (60 * cdate.min) + cdate.sec
	
	-- based on the current date, calculate the current day we are on
	-- (note, that between midnight and 6am we consider it "yesterday")
	-- (this means that media lists are made each day for 6am to 5:59am (next day))
	if cdate.hour <= 6 then
		rseed = (cdate.yday-1) + ((cdate.year - 2012 + (100 * channum)) * 366)
	else
		rseed = cdate.yday + ((cdate.year - 2012 + (100 * channum)) * 366)
	end

	-- seed the random number with the current day we're on...
	-- (ensures a unique program schedule every day forever)
	math.randomseed(rseed)

	-- shuffle the fullist
	for i = nfulllist, 1, -1 do -- backwards
		local r = math.random(nfulllist) -- select a random number between 1 and i
		fulllist[i], fulllist[r] = fulllist[r], fulllist[i] -- swap the randomly selected item to position i
	end 

	-- STEP 3. START LOADING IN VIDEO FILES UNTIL WE GET TO THE CURRENT TIME

	-- current time of the channel
	last_duration = 0
	total_duration = 0
	curidx = 1

	-- debug
	--vlc.msg.info( "!!!DEBUG!!! csec: " .. tostring(csec) )

	-- loop forever...
	while true do
		-- if we are currently probing past the end of the fulllist
		if curidx > nfulllist then
			curidx = 1
		end

		-- add the duration of the probed item to the total
		if fulllist[curidx].duration ~= nil then
			last_duration = total_duration
			total_duration = last_duration + fulllist[curidx].duration
		end
		
		--debug
		--vlc.msg.info( "!!!ADDING!!! "..fulllist[curidx].path.." dur: " .. tostring(total_duration) )

		-- see if we're now past the current time
		if total_duration > csec then
			break -- we're done
		end

		-- increment the index of the probe item
		curidx = curidx + 1
	end

	-- STEP 4. LOAD THE FIRST ITEM INTO THE PLAYLIST AT CURRENT TIME

	-- start with a blank playlist
	playlist = {}

	-- the start time will be the last duration minus the current seconds
	start_time = csec - last_duration

	-- make sure we have a valid start time
	if start_time < 0 then
		start_time = 0
	end	

	-- add the start/stop time properties
	fulllist[curidx].options = {}
	table.insert(fulllist[curidx].options, "start-time="..tostring(start_time))
	table.insert(fulllist[curidx].options, "stop-time="..tostring(fulllist[curidx].duration))

	-- add the item to the playlist as the first item
	table.insert( playlist, fulllist[curidx] )


	-- STEP 5. ADD IN ALL REMAINING ITEMS UNTIL WE HIT A 30 HR PLAYLIST

	-- now loop until we hit 24 hrs + 6 hrs
	while true do
		-- increment the current index
		curidx = curidx + 1

		-- if we are currently probing past the end of the fulllist
		if curidx > nfulllist then	
			curidx = 1
		end

		if fulllist[curidx].duration ~= nil then

			-- add the next item to the playlist
			table.insert( playlist, fulllist[curidx] )

			-- update the duration
			total_duration = total_duration + fulllist[curidx].duration

		end

		-- check if we're past 30 hours yet
		if total_duration > 0 then
			break
		end	
	end

	-- give VLC the playlist
	return playlist
end

