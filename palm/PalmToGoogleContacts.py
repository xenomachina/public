#!/usr/bin/python

import sys
import csv

# http://sourceforge.net/projects/pythonpalmdb/files/PalmDB/PalmDB_1_8_1/
import PalmDB

# http://pastebin.com/f75a93f48
import PalmAddress

"""
Reads Palm AddressDB.pdb from stdin and converts it into a CSV file
suitable for importing into Google Contacts.

This was a one-off script. I used it to migrate my contacts from my old
Palm Treo to my Android phone (which uses Google Contacts for its
phonebook). Because of that, there are some weird special cases. (How it
deals with Canadian addresses, for example.)

You may need to do some tweaking to get it to do what you want, and/or
tweak the generated CSV. A spreadsheet (perhaps Google Docs) works well
for the latter.
"""

STATE_CODES = {
  'ALABAMA': 'AL',
  'ALASKA': 'AK',
  'AMERICAN SAMOA': 'AS',
  'ARIZONA': 'AZ',
  'ARKANSAS': 'AR',
  'CALIFORNIA': 'CA',
  'COLORADO': 'CO',
  'CONNECTICUT': 'CT',
  'DELAWARE': 'DE',
  'DISTRICT OF COLUMBIA': 'DC',
  'FEDERATED STATES OF MICRONESIA': 'FM',
  'FLORIDA': 'FL',
  'GEORGIA': 'GA',
  'GUAM': 'GU',
  'HAWAII': 'HI',
  'IDAHO': 'ID',
  'ILLINOIS': 'IL',
  'INDIANA': 'IN',
  'IOWA': 'IA',
  'KANSAS': 'KS',
  'KENTUCKY': 'KY',
  'LOUISIANA': 'LA',
  'MAINE': 'ME',
  'MARSHALL ISLANDS': 'MH',
  'MARYLAND': 'MD',
  'MASSACHUSETTS': 'MA',
  'MICHIGAN': 'MI',
  'MINNESOTA': 'MN',
  'MISSISSIPPI': 'MS',
  'MISSOURI': 'MO',
  'MONTANA': 'MT',
  'NEBRASKA': 'NE',
  'NEVADA': 'NV',
  'NEW HAMPSHIRE': 'NH',
  'NEW JERSEY': 'NJ',
  'NEW MEXICO': 'NM',
  'NEW YORK': 'NY',
  'NORTH CAROLINA': 'NC',
  'NORTH DAKOTA': 'ND',
  'NORTHERN MARIANA ISLANDS': 'MP',
  'OHIO': 'OH',
  'OKLAHOMA': 'OK',
  'OREGON': 'OR',
  'PALAU': 'PW',
  'PENNSYLVANIA': 'PA',
  'PUERTO RICO': 'PR',
  'RHODE ISLAND': 'RI',
  'SOUTH CAROLINA': 'SC',
  'SOUTH DAKOTA': 'SD',
  'TENNESSEE': 'TN',
  'TEXAS': 'TX',
  'UTAH': 'UT',
  'VERMONT': 'VT',
  'VIRGIN ISLANDS': 'VI',
  'VIRGINIA': 'VA',
  'WASHINGTON': 'WA',
  'WEST VIRGINIA': 'WV',
  'WISCONSIN': 'WI',
  'WYOMING': 'WY',
}


FIELD_NAMES = [
  'Name',
  'Given Name',
  'Additional Name',
  'Family Name',
  'Yomi Name',
  'Given Name Yomi',
  'Additional Name Yomi',
  'Family Name Yomi',
  'Name Prefix',
  'Name Suffix',
  'Initials',
  'Nickname',
  'Short Name',
  'Maiden Name',
  'Birthday',
  'Gender',
  'Location',
  'Billing Information',
  'Directory Server',
  'Mileage',
  'Occupation',
  'Hobby',
  'Sensitivity',
  'Priority',
  'Subject',
  'Notes',
  'Group Membership',
  'E-mail 1 - Type',
  'E-mail 1 - Value',
  'E-mail 2 - Type',
  'E-mail 2 - Value',
  'E-mail 3 - Type',
  'E-mail 3 - Value',
  'E-mail 4 - Type',
  'E-mail 4 - Value',
  'IM 1 - Type',
  'IM 1 - Service',
  'IM 1 - Value',
  'Phone 1 - Type',
  'Phone 1 - Value',
  'Phone 2 - Type',
  'Phone 2 - Value',
  'Phone 3 - Type',
  'Phone 3 - Value',
  'Address 1 - Type',
  'Address 1 - Formatted',
  'Address 1 - Street',
  'Address 1 - City',
  'Address 1 - PO Box',
  'Address 1 - Region',
  'Address 1 - Postal Code',
  'Address 1 - Country',
  'Address 1 - Extended Address',
  'Organization 1 - Type',
  'Organization 1 - Name',
  'Organization 1 - Yomi Name',
  'Organization 1 - Title',
  'Organization 1 - Department',
  'Organization 1 - Symbol',
  'Organization 1 - Location',
  'Organization 1 - Job Description',
  'Website 1 - Type',
  'Website 1 - Value',
]

def warnIfSet(contact, name, value):
  if value:
    print >>sys.stderr, "WARNING: ignoring %r's value in %s field: %r" % (
        ' '.join(x for x in (contact.forename, contact.surname) if x), name, value)

PHONE_TYPE_MAP = {
  PalmAddress.PHONE_WORK   : "Work",
  PalmAddress.PHONE_HOME   : "Home",
  PalmAddress.PHONE_FAX    : "Fax",
  PalmAddress.PHONE_OTHER  : "Other",
  #PalmAddress.PHONE_EMAIL intentionally left out
  PalmAddress.PHONE_MAIN   : "Main",
  PalmAddress.PHONE_PAGER  : "Pager",
  PalmAddress.PHONE_MOBILE : "Mobile"
}

if __name__ == '__main__':
  db = PalmDB.PalmDatabase.PalmDatabase()
  db.fromByteArray(sys.stdin.read())

  out = csv.writer(sys.stdout)
  out.writerow(FIELD_NAMES)
  n = 0
  for record in db:
    contact = PalmAddress.PalmAddress(record.toByteArray(0)[1])

    phones = []
    emails = []
    assert len(contact.phoneLabels) == len(contact.phones)
    for phlabel, phnumber in zip(contact.phoneLabels, contact.phones):
      if phnumber:
        if phlabel == PalmAddress.PHONE_EMAIL:
          emails.append(phnumber)
        else:
          phones.append((PHONE_TYPE_MAP[phlabel], phnumber))

    for ignored_phone in phones[3:]:
      warnIfSet(contact, 'phone', ignored_phone)
    phones += [('','')] * 3
    phones = phones[:3]

    for ignored_email in emails[4:]:
      warnIfSet(contact, 'email', ignored_phone)
    emails += [''] * 4
    emails = emails[:4]

    def join_nonempty(delimiter, seq):
      return delimiter.join(x for x in seq if x)

    if contact.state and contact.state.upper() in STATE_CODES:
      contact.state = STATE_CODES[contact.state.upper()]

    if contact.country and contact.country.upper() == 'CANADA':
      formatted_address = join_nonempty('\n', (
            contact.address,
            join_nonempty(', ', (
              contact.city,
              contact.state,
              contact.country)),
            contact.zipCode))
    else:
      formatted_address = join_nonempty('\n', (
            contact.address,
            join_nonempty('  ', (
              join_nonempty(', ', (
                contact.city,
                contact.state)),
              contact.zipCode)),
            contact.country))
    out.writerow((
        # Name
        ' '.join(x for x in (contact.forename, contact.surname) if x), 
        # Given Name
        contact.forename,
        # Additional Name
        '',
        # Family Name
        contact.surname,
        # Yomi Name
        '',
        # Given Name Yomi
        '',
        # Additional Name Yomi
        '',
        # Family Name Yomi
        '',
        # Name Prefix
        '',
        # Name Suffix
        '',
        # Initials
        '',
        # Nickname
        '',
        # Short Name
        '',
        # Maiden Name
        '',
        # Birthday
        '',
        # Gender
        '',
        # Location
        '',
        # Billing Information
        '',
        # Directory Server
        '',
        # Mileage
        '',
        # Occupation
        '',
        # Hobby
        '',
        # Sensitivity
        '',
        # Priority
        '',
        # Subject
        '',
        # Notes
        contact.note,
        # Group Membership
        '',
        # E-mail 1 - Type
        ('' if not emails[0] else '*'),
        # E-mail 1 - Value
        emails[0],
        # E-mail 2 - Type
        '',
        # E-mail 2 - Value
        emails[1],
        # E-mail 3 - Type
        '',
        # E-mail 3 - Value
        emails[2],
        # E-mail 4 - Type
        '',
        # E-mail 4 - Value
        emails[3],
        # IM 1 - Type
        '',
        # IM 1 - Service
        '',
        # IM 1 - Value
        '',
        # Phone 1 - Type
        phones[0][0],
        # Phone 1 - Value
        phones[0][1],
        # Phone 2 - Type
        phones[1][0],
        # Phone 2 - Value
        phones[1][1],
        # Phone 3 - Type
        phones[2][0],
        # Phone 3 - Value
        phones[2][1],
        # Address 1 - Type
        '',
        # Address 1 - Formatted
        formatted_address,
        # Address 1 - Street
        contact.address,
        # Address 1 - City
        contact.city,
        # Address 1 - PO Box
        '',
        # Address 1 - Region
        contact.state,
        # Address 1 - Postal Code
        contact.zipCode,
        # Address 1 - Country
        contact.country,
        # Address 1 - Extended Address
        '',
        # Organization 1 - Type
        '',
        # Organization 1 - Name
        contact.company,
        # Organization 1 - Yomi Name
        # Organization 1 - Title
        contact.title,
        # Organization 1 - Department
        '',
        # Organization 1 - Symbol
        '',
        # Organization 1 - Location
        '',
        # Organization 1 - Job Description
        '',
        # Website 1 - Type
        '',
        # Website 1 - Value
        '',
      ))

    warnIfSet(contact, 'custom[0]', contact.custom[0])
    warnIfSet(contact, 'custom[1]', contact.custom[1])
    warnIfSet(contact, 'custom[2]', contact.custom[2])
    warnIfSet(contact, 'custom[3]', contact.custom[3])
    n += 1

  print >>sys.stderr, '%s contacts converted' % n
  del out
  sys.stdout.flush()
