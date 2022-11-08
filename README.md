# USAC Data cleaner
Clean race registration and team member data
Example, test data and mockup.
[Google Sheet](https://docs.google.com/spreadsheets/d/1Xaw3gEl4WuGme9diHiyPtDFCEmKtZJ5P9Qgk2bRsS5k/edit?usp=sharing)

### Comparison Rules:
#### License errors
- Missing or license does not exist: Suggest to match using any two of (LastName, email, phone, dob, zipcode)
- License valid but one of these does not match one or more of (last name, dob). Show/suggest matching license profile.
- License valid but expired: Show experation date
- 
#### Weak rules
- License valid and last name or DOB matches: One or more of the folloing does not match [email, phone, zipcode]
