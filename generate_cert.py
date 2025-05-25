from OpenSSL import crypto
import os

def create_self_signed_cert():
    # Créer le répertoire ssl s'il n'existe pas
    if not os.path.exists('Reserv_hotel/ssl'):
        os.makedirs('Reserv_hotel/ssl')

    # Générer une nouvelle paire de clés
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    # Créer un certificat auto-signé
    cert = crypto.X509()
    cert.get_subject().C = "FR"
    cert.get_subject().ST = "State"
    cert.get_subject().L = "City"
    cert.get_subject().O = "Organization"
    cert.get_subject().OU = "Organizational Unit"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)  # Valide pour 1 an
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    # Sauvegarder la clé privée
    with open("Reserv_hotel/ssl/private.key", "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    # Sauvegarder le certificat
    with open("Reserv_hotel/ssl/certificate.crt", "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

if __name__ == '__main__':
    create_self_signed_cert() 