import asyncio
import discord

class ClientManager():
	def __init__(self):
		self.client = None
		self.quit_now = False
		self.selected_server = "No server selected"
		self.selected_channel = -1

	# coroutines here
	async def get_servers_coro(self):
		print("Getting server list from Discord, please be patient...")
		await self.client.wait_until_ready()
		servers = self.client.servers
		return servers

	async def print_servers_coro(self):
		servers = await self.get_servers_coro()
		for server in servers:
			print(server.id, server.name)
		await self.client.logout()

	async def get_channels_coro(self):
		servers = await self.get_servers_coro()
		try:
			server = [server for server in servers if server.name == self.selected_server][0]
			channels = server.channels
			return list(channels)
		except IndexError:
			print("No server with that name found")
			return None

	async def print_channels_coro(self):
		channels = await self.get_channels_coro()
		if channels:
			for i in range(len(channels)):
				print(i, channels[i].name)
		else:
			print("Not listing channels because the channel couldn't be retrieved")
		await self.client.logout()

	async def delete_server_coro(self):
		channels = await self.get_channels_coro()
		if not channels:
			print("Server with this name not found")
			await self.client.logout()
			return

		response = input("Delete ALL messages from " + self.selected_server + "? Type YES (enter) to confirm: ")
		if response != "YES":
			print("We didn't get the go-ahead so we aren't deleting everything")
			await self.client.logout()
			return

		failed_channels = []
		for i in range(len(channels)):
			self.selected_channel = i
			failure = await self.delete_channel_coro(True)
			if failure:
				failed_channels.append(failure)
		
		if failed_channels:
			print("These channels weren't deleted successfully:")
			for i in range(len(failed_channels)):
  				print(failed_channels[i])
		await self.client.logout()

	async def delete_channel_coro(self, called_from_server_delete=None):
		channels = await self.get_channels_coro()
		if not channels:
			print("Server with this name not found")
			await self.client.logout()
			return

		try:
			current_channel = channels[self.selected_channel]
			print("Channel:", current_channel.name)
		except IndexError:
			print("channel index " + str(self.selected_channel) + " not in server " + server_name)
			await self.client.logout()
			return

		if called_from_server_delete is None:
			response = input("Delete all messages in " + current_channel.name + "? Type YES (enter) to confirm: ")
			if response != "YES":
				print("We didn't get the go-ahead so we aren't deleting everything")
				await self.client.logout()
				return

		count = 0
		try:
			print("Now deleting messages...")
			async for message in self.client.logs_from(current_channel, limit=1000000):
				if (message.author == self.client.user):
					count += 1
					if count % 100 == 0:
						print(str(count) + " messages deleted so far...")
					await self.client.delete_message(message)
			print("Deleted " + str(count) + " messages from channel " + current_channel.name)
		except:
			print("Didn't manage to successfully delete from " + current_channel.name)
			return current_channel.name

		if called_from_server_delete is None:
			await self.client.logout()

	"""
	This function gets stuff from the discord. It logs in and logs out for each
	operation because I can't figure out how to pass control back without
	logging out lol. I only know so much :confounded:
	Uh anyway, this function accepts an async function with no arguments
	"""
	def run_coroutine(self, coro):
		asyncio.set_event_loop(asyncio.new_event_loop())
		self.client = discord.Client()
		self.client.loop.create_task(coro())
		self.client.run(self.email, self.password)

	#These functions pass the coroutines to self.run_coroutine
	def print_servers(self):
		self.run_coroutine(self.print_servers_coro)

	def print_channels(self):
		self.run_coroutine(self.print_channels_coro)

	def delete_server_messages(self):
		self.run_coroutine(self.delete_server_coro)

	def delete_channel_messages(self):
		self.run_coroutine(self.delete_channel_coro)


	#menu here
	def menu_quit(self):
		self.quit_now = True

	def menu_select_server(self):
		response = input("Which server do you want to select? Please enter the server's NAME: ")
		#if you have two servers with the same name I can't help you sorry
		self.selected_server = response
		print("\nServer name has been set to: " + response)

	def menu_select_channel(self):
		response = input("Which channel do you want to select? Please enter the channel's NUMBER: ")
		try:
			self.selected_channel = int(response)
			print("\nChannel number has been set to: " + response)
		except:
			print("\nDidn't get a number. Please enter a number, not the channel name.")

	def menu_main(self):
		response = input(
			"\nLet's delete our discord history!\n\n"
			"1. Select a server\n"
			"2. Select a channel\n"
			"3. Print a list of all servers this account has joined\n"
			"4. Print a list of all channels on the selected server\n"
			"5. Delete all messages on the selected server (wow!)\n"
			"6. Delete all messages in the selected channel on the selected server\n"
			"7. Quit\n\n"

			"Currently selected server: %s\n"
			"Currently selected channel: %s\n\n"
			
			"Just type in the number and press enter\n"
			% (self.selected_server, self.selected_channel)
		)

		funcs = {
			"1" : self.menu_select_server,
			"2" : self.menu_select_channel,
			"3" : self.print_servers,
			"4" : self.print_channels,
			"5" : self.delete_server_messages,
			"6" : self.delete_channel_messages,
			"7" : self.menu_quit,
		}

		try:
			return funcs[response]
		except KeyError:
			print("Hey sorry that wasn't a correct choice can you try again")
			return None
		except:
			print("Holy crap how did you get here lol")

	def menu_loop(self):
		while not self.quit_now:
			func = self.menu_main()
			if func:
				func()

	def menu_credentials(self):
		#If you wanna submit a pull request to improve this section please do
		print("This is totally insecure don't run it on a public computer lol")
		self.email = input("Enter your Discord e-mail address/account login: ")
		self.password = input("Enter your Discord password: ")

dog = ClientManager()
dog.menu_credentials()
dog.menu_loop()
