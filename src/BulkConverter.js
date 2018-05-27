var xhttp = new XMLHttpRequest();

async function bulkConvert()
{
   var urls = document.getElementById("urls").value;
   var urlsSpl = urls.split("\n");

   var waitTime = (urlsSpl.length * 1000) > 20000 ? 20000 : (urlsSpl.length * 1000) < 8000 ? 8000 : (urlsSpl.length * 1000);

   for (i = 0; i < urlsSpl.length; i++)
   {
      if (urlsSpl[i] != null && urlsSpl[i] != "")
      {
         convert(urlsSpl[i]);
         await sleep(waitTime);
      }
   }

   await sleep((waitTime + 1000) < 8000 ? 8000 : (waitTime + 1000));
   alert("All done!");
   document.getElementById("urls").value = "";
}

function convert(url)
{
   xhttp.open("POST", "http://convert2mp3.net/en/index.php?p=convert", true);
   xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
   xhttp.send("quality=1&format=mp3&9di2n3=" + document.getElementById("tok").value + "&url=" + url);

   xhttp.onreadystatechange = function()
   {
      if (xhttp.readyState == 4 && xhttp.status == 200)
      {
         var init = xhttp.responseText;
         var newUrl = init.substring(init.indexOf("http://c-api"), init.lastIndexOf("style=") - 2);

         if (newUrl != "" && newUrl != null)
         {
            step2(newUrl);
         }
      }
   };
}

function step2(url)
{
   xhttp.open("GET", url, true);
   xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
   xhttp.send();
   xhttp.onreadystatechange = function()
   {
      if (xhttp.readyState == 4 && xhttp.status == 200)
      {
         var init = xhttp.responseText;
         var newUrl = init.substring(init.indexOf("http://convert2mp3.net"), init.indexOf("\";")).replace("tags", "complete");

         step3(newUrl);
      }
   };
}

function step3(url)
{
   xhttp.open("GET", url, true);
   xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
   xhttp.send();
   xhttp.onreadystatechange = function()
   {
      if (xhttp.readyState == 4 && xhttp.status == 200)
      {
         var init = xhttp.responseText;
         var newUrl = init.substring(init.indexOf("http://cd"), init.indexOf("&d=y")) + "&d=y"; // "&.mp3"

         if (newUrl != "D:/&d=y" && newUrl != "&d=y" && newUrl != "/&d=y")
         {
            download(newUrl);
         }

      }
   };
}

function download(url)
{
   window.parent.location.href = url;
}

function sleep(ms)
{
   return new Promise(resolve => setTimeout(resolve, ms));
}