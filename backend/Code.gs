function doGet(e) {
  const type = e.parameter.type;
  const to = e.parameter.to;
  const name = e.parameter.name;
  const code = e.parameter.code;
  const link = e.parameter.link;
  const cc = e.parameter.cc;
  const reservationId = e.parameter.reservationId;
  const htmlBody = e.parameter.htmlBody;
  
  // Handle based on type of email
  if (type === "verification") {
    MailApp.sendEmail({
      to: to,
      subject: "[DO NOT REPLY] UP NISMED Hostel - Verification Code",
      htmlBody:
        `<p>Thank you for your reservation, ${name}!</p>` +
        `<p>Click to verify: <a href="${link}">${link}</a></p>` +
        `<p>Your code: <b>${code}</b></p>`
    });
  } else if (type === "confirmation") {
    MailApp.sendEmail({
      to: to,
      cc: cc,
      subject: `#${reservationId} Reservation Confirmed`,
      htmlBody: htmlBody
    });
  }

  return ContentService.createTextOutput("Email sent")
                       .setMimeType(ContentService.MimeType.TEXT);
}

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
      subject: `Reservation #${data.reservationId} Confirmed`,
      htmlBody: data.htmlBody,
      name: "UP NISMED Hostel"
    });
  }

  return ContentService.createTextOutput("OK");
}
