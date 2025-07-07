function doPost(e) {
  /*
  This function serves as the API endpoint for sending emails (post request)
  It expects the following request:
  {
    'type': '...',
    'name': '...',
    'link': '...',
    'code': '...',
    'to': 'xyz@example.com'
    'cc': 'xyz@example.com',
    'htmlBody': '...'
  }
  */
  const data = JSON.parse(e.postData.contents);
  const type = data.type;

  if (type === "verification") {
    MailApp.sendEmail({
      to: data.to,
      subject: "UP NISMED Hostel - Verification Code",
      htmlBody: `
        <p>Thank you for your reservation at UP NISMED Hostel, ${data.name}!</p>
        <p>Please verify your reservation by clicking the link below:<br>
        <a href="${data.link}">${data.link}</a></p>
        <p>verification code is <u><strong>${data.code}</strong></u></p>`,
      name: "UP NISMED Hostel"
    });
  }

  if (type === "confirmation") {
    MailApp.sendEmail({
      to: data.to,
      cc: data.cc,
      subject: `Successful Reservation - UP NISMED Hostel`,
      htmlBody: data.htmlBody,
      name: "UP NISMED Hostel"
    });
  }

  return ContentService.createTextOutput("OK");
}
