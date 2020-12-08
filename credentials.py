"""UserIDs and Passwords should be entered within inverted commas. """

class Credentials:
    """ Credentials class holds the GLA Portal's and Zoom User IDs and PAsswords."""

    def get_GLA_UserID():
        """returns the university roll number"""
        return "" #Enter your own GLA Uni Roll Number

    def get_GLA_Password():
        """returns the GLA Portal's password"""
        return "" #Enter your own GLA Uni Portal Password

    def get_Zoom_UserID():
        """returns the email ID associated with zoom"""
        return "" #Enter your email ID associated with zoom account

    def get_Zoom_Password():
        """returns the password associated with zoom id"""
        return "" 

if __name__ == '__main__':
    print(Credentials.get_GLA_UserID(),Credentials.get_GLA_Password(),Credentials.get_Zoom_UserID(),Credentials.get_Zoom_Password(),sep = '\n')
    