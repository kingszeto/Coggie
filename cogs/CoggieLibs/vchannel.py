import discord

# a regular linked list
class VoiceChannelLL():
    def __init__(self, channel: discord.VoiceChannel, vnext=None):
        self.voice_channel = channel
        self.next = vnext
    
    def empty(self):
        current = self
        while current:
            if current.voice_channel.members:
                return False
            current = current.next
        return True

    def __contains__(self, item: discord.Member):
        current = self
        if isinstance(item, discord.Member):
            while current:
                if item in current.voice_channel.members:
                    return True
                current = current.next
        elif isinstance(item, discord.VoiceChannel):
            while current:
                if item == current.voice_channel:
                    return True
                current = current.next
        return False

# wrapper for VoiceChannelLL but honestly it's becoming spaghetti code
class CoggieVoice():
    def __init__(self, creator: discord.Member, channels: VoiceChannelLL):
        self.creator = creator
        self.channels = VoiceChannelLL(channels)

    def has_members(self):
        return not self.channels.empty()
            
