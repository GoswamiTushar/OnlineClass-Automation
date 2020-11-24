class Credentials:

	def get_GLA_UserID():
		return ""

	def get_GLA_Password():
		return ""

	def get_Zoom_UserID():
		return ""

	def get_Zoom_Password():
		return ""

if __name__ == '__main__':
	print(Credentials.get_GLA_UserID(), Credentials.get_GLA_Password(), Credentials.get_Zoom_UserID(), Credentials.get_Zoom_Password(), sep = '\n')
	