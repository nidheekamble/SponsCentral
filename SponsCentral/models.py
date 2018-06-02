from SponsCentral import db

class PartyUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String(30), unique=True, nullable=False)
    party_email= db.Column(db.String(120), unique=True, nullable=False)
    party_type = db.Column(db.String(20), unique= False, nullable= False)
    party_kind = db.Column(db.String(20), unique= False, nullable= False)
    party_contactNo1 = db.Column(db.Integer, unique = True , nullable = False)
    party_contactNo2= db.Column(db.Integer, unique = True , nullable = True)
    party_address = db.Column(db.String(300), unique=True, nullable=False)
    party_about = db.Column(db.String(1500), unique=True, nullable=False)
    party_fromAmount = db.Column(db.Integer, unique = False , nullable = False)
    party_toAmount = db.Column(db.Integer, unique = False , nullable = False)
    party_logo = db.Column(db.String(20), unique= False, nullable= True, default = 'default.jpeg' )# check on the nullable field
    def __repr__(self):
        return f"PartyUser('{self.party_name}','{self.party_email}','{self.party_type}','{self.party_kind}','{self.party_contactNo1}','{self.party_contactNo2}','{self.party_address}','{self.party_about}','{self.party_fromAmount}','{self.party_toAmount}','{self.party_logo}')"


class SponsorUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String(30), unique=True, nullable=False)
    party_email= db.Column(db.String(120), unique=True, nullable=False)
    party_type = db.Column(db.String(20), unique= False, nullable= False)
    party_kind = db.Column(db.String(20), unique= False, nullable= False)
    party_contactNo1 = db.Column(db.Integer, unique = True , nullable = False)
    party_contactNo2= db.Column(db.Integer, unique = True , nullable = True)
    party_address = db.Column(db.String(300), unique=True, nullable=False)
    party_about = db.Column(db.String(1500), unique=True, nullable=False)
    party_fromAmount = db.Column(db.Integer, unique = False , nullable = False)
    party_toAmount = db.Column(db.Integer, unique = False , nullable = False)
    party_logo = db.Column(db.String(20), unique= False, nullable= True, default = 'default.jpeg' )# check on the nullable field
    def __repr__(self):
        return f"SponsorUser('{self.sponsor_name}','{self.sponsor_email}','{self.sponsor_type}','{self.sponsor_kind}','{self.sponsor_contactNo1}','{self.sponsor_contactNo2}','{self.sponsor_address}','{self.sponsor_about}','{self.sponsor_fromAmount}','{self.sponsor_toAmount}','{self.sponsor_logo}')"
