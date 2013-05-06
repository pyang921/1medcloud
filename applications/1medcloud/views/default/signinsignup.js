// JavaScript Document
function psignin()
{
  document.patientsignin.submit();
}

function psignup()
{
  document.patientsignup.submit();
  response=HTTP.GET(result);
  alert(response);
}