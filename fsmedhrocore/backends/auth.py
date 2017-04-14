import ldap
from django.contrib.auth.models import User
from django.conf import settings

class LdapUniHro(object):
    """
    """
    BASE_DN = "ou=people,o=uni-rostock,c=de"
    HOST = "ldaps://ldap.uni-rostock.de"

    def authenticate(self, username, password):

        # nur lowercase um Duplikationen zu verhindern
        username = username.lower()

        user_dn = "uid=%s,%s" % (username, self.BASE_DN)
        conection = ldap.initialize(self.HOST)

        try:
            try:
                conection.bind_s(user_dn, password)
            except ldap.INVALID_CREDENTIALS:
                return None  # throw error?
            except ldap.LDAPError as e:
                return None
            else:
                ldapuser = conection.search_s("ou=people,o=uni-rostock,c=de", ldap.SCOPE_SUBTREE, "uid="+username)[0][1]
        finally:
            conection.unbind()

        if settings.DEBUG:
            print('Loginversuch, LDAP-Daten:')
            for att in ldapuser:
                for item in ldapuser[att]:
                    print(att, ':', item.decode())


        if validate_ladp_user(ldapuser):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. password won't be used for authentification
                user = User(username=username, password='get from LDAP')
                user.is_staff = False
                user.is_superuser = False
                user.set_unusable_password()
                user.save()

            if user.is_active:
                # Update User-Data
                user.email = ldapuser["mail"][0].decode()
                user.last_name = ldapuser["sn"][0].decode()
                user.first_name = ldapuser["givenName"][0].decode()
                user.save()
                return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def validate_ladp_user(ldapuseratts):
    ldap_auth_filter = {
        "employeeType": "s",
        "uniRFaculty": "03",
        "gidNumber": "97"
    }

    for key, value in ldap_auth_filter.items():
        # if there is no matching in one filter-row, return False
        if any(item.decode() == value for item in ldapuseratts[key]):
            return True

    return False
