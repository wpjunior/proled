## Script (Python) "register"
##title=Register a user
##parameters=password='password', confirm='confirm'
REQUEST=context.REQUEST
portal_properties = context.portal_properties
portal_registration = context.portal_registration

if not portal_properties.validate_email:
  failMessage = portal_registration.testPasswordValidity(password, confirm)
  if failMessage:
      REQUEST.set( 'error', failMessage )
      return context.join_form( context, REQUEST, error=failMessage )
      
failMessage = portal_registration.testPropertiesValidity(REQUEST)

if failMessage:
    REQUEST.set( 'error', failMessage )
    return context.join_form( context, REQUEST, error=failMessage )
else:
    password=REQUEST.get('password') or portal_registration.generatePassword()
    portal_registration.addMember(REQUEST['username'], password, properties=REQUEST, REQUEST=REQUEST)

    if portal_properties.validate_email or REQUEST.get('mail_me', 0):
        portal_registration.registeredNotify(REQUEST['username'])

    return context.registered( context, REQUEST )
