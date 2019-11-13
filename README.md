# Icon-Icons-Downloader
Automatically download icon packs from https://icon-icons.com/  and convert them into .ico, .svg and .png format
</br></br>
<img src="https://i.gyazo.com/12d82c3e49a12db7e26b43736726d4ee.png"></img>
<img src="https://i.gyazo.com/b375156ea0298fe1f4dd07adb08060b1.png"></img>
</br></br>
<b>Code</b></br>
The downloader is based on Python but compiled to executable for easier usage without the need to install all libraries dependancies.
<br><br>
<b>What it does?</b></br>
The program is capable to download multiple icon packs automatically via pre-set icon range or list. It can also convert them from .png to 128 pixels .svg and .ico 16x16-128x128 32bit.

<b>Reason for the program</b></br>
First of all, learning new things, expertise in automation and lastly.. I am looking very often for icon packs for my projects but it's somethimes hard to find big icon packs with more 100+  sharing the same design. Even if you find a website that will give you an option to download the whole icon pack it's very likely that it will be only png not ico and svg, so you will have to convert them afterwards which is twice as much work. There are many websites that provide paid downloading service but that was not the point here since there are pleny free anyway. 

I found https://icon-icons.com/ to be very nice website with a big icon database but unfortrunatelly you can not download the whole pack at once, which is very bad especially if you need all icons you have to download them one by one. So I decided create a program to automate the proccess.

<b>Requirements</b>
  - Having Windows OS
  - Install Microsoft Visual C++ *inclided in the package
  - Chrome Browser -> Must be up to date
  - Chromedriver -> https://chromedriver.chromium.org/ Included in the pack, but make sure it is up to date
  
<b>Usability</b>
All you need ot do is to add the icon pack that you need in the "Download List", check the boxes if you want along with all png icons also ico and svg, select the download folder and press the "Start" button. The GUI window will be closed and console window will be opened where you can see the logs.

<b>How to add Icon-Pack</b>
The program can scrape all available icons in the website with selecting the range from 1 to 2000 and leaving the download list empty for example, but if you need particular icon list you can list them one by one with a coma delimiter in the downloading list.

You have to list the icon pack number not name -> <img src="https://i.gyazo.com/bdccaa577875877cdf1d18b34908daa0.png"></img> in this case it's <b>2080</b>. So if we need to download icon packs 56 and 2079 you list them as <b>56,2079</b> then the range will not work and the proggram will proceed with the list.

<b>*Importnat:</b><i> Please keep in mind that if you have listed something in the download list it will be in priority, so the range wont work until the list is completed. </i>

