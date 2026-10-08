This article describes problems where Firefox cannot load websites but other Web browsers (such as **[Windows]** Microsoft Edge or Internet Explorer **[macOS]** Safari **[Linux]** Epiphany on Gnome or Konqueror on KDE ) can. When this happens, Firefox may show a *Server not found* or *Unable to connect* error message.

* For other error messages that display when you try to view websites in Firefox, see Websites don't load - troubleshoot and fix error messages.
* If none of the Web browsers on your computer can load websites, see Firefox and other browsers can't load websites.

# Internet Security software blocking Firefox

If you were able to load websites until you updated Firefox or until your Internet security software was updated, reconfigured or a new one was added, your Internet security software (including firewalls, antivirus programs, anti-spyware programs, and more) is likely preventing Firefox from connecting to the Internet.

**Note:** Some Internet security programs can block Internet access even when they are disabled.

So, you should make sure your Internet security software is up-to-date and remove Firefox from your program's list of trusted or recognized programs, then add it back. For instructions on how to configure some programs, see Configure firewalls so that Firefox can access the Internet.

# Firefox connection settings

If you connect to the Internet through a proxy server that is having connection problems, you will not be able to load websites. To check your connection settings in Firefox:

1. **[macOS]** In the Menu bar at the top of the screen, click Firefox and select Settings (or Preferences, in some cases). **[Windows / Linux]** Click the menu button  and select Settings.
2. In the General panel, go to the *Network Settings* *Proxy settings*  section Select Privacy and security, go to the *Connection and software security* section and click Advanced settings .
3. Go to **Proxy settings** and click Click Settings…   Configure proxy . The Connection Settings dialog will open.
4. Change your proxy settings:
   * If you don't connect to the Internet through a proxy (or don't know whether you connect through a proxy), select **No Proxy**.
   * If you connect to the Internet through a proxy, compare Firefox's settings to another browser's (which is working normally).
5. Close the *Connection Settings* dialog.
6. Close the Settings page. Any changes you've made will automatically be saved.

**Note:** If you find that changes you make to your Firefox connection settings are not remembered when you restart Firefox, see How to fix preferences that won't save.

# IPv6

Firefox supports IPv6 by default, which may cause connection problems on certain systems. To disable IPv6 in Firefox:

**Warning:** These instructions are for experienced Firefox users. Changing settings in the Configuration Editor (*about:config*) can have serious effects on your browser’s stability, security and performance.

**Only proceed if you are comfortable with advanced settings and understand the potential impacts**.

1. Type **about:config** in the address bar and press **[Windows / Linux]** Enter **[macOS]** Return .
   A warning page may appear. Click Accept the Risk and Continue to go to the *about:config* page.
2. Enter **network.dns.disableIPv6** in the search field.
3. In the list of preferences click the *Toggle*  button next to network.dns.disableIPv6 to set its value to true.

# DNS Prefetching

Firefox attempts to speed up loading new websites by using DNS Prefetching, which can cause page load errors with some system configurations. To disable DNS Prefetching:

**Warning:** These instructions are for experienced Firefox users. Changing settings in the Configuration Editor (*about:config*) can have serious effects on your browser’s stability, security and performance.

**Only proceed if you are comfortable with advanced settings and understand the potential impacts**.

1. Type **about:config** in the address bar and press **[Windows / Linux]** Enter **[macOS]** Return .
   A warning page may appear. Click Accept the Risk and Continue to go to the *about:config* page.
2. Enter **network.dns.disablePrefetch** in the search field.
   * If such preference doesn't already exist, select **Boolean** and click the *Add*  button.
3. Click the *Toggle*  button to set the preference value to true, if it's not already set.

# Firefox cannot load certain websites

If you find that Firefox can load some websites but not others, first clear your Firefox cookies and cache:

1. Click the menu button  to open the menu panel.
2. Click History and select Clear recent history…
3. In the *When:* drop-down, select **Everything**.
4. Below the drop-down menu, select both **Cookies and site data** and **Temporary cached files and pages**. Make sure other items you want to keep are not selected.
5. Click Clear.

## Check for malware

If clearing the cookies and cache didn't help, you should check your computer for malware. Certain types of malware are known to target Firefox and can prevent it from loading various websites:

* If you have an antivirus or Internet security program, update its detections database and do a full scan of your system.
* If you still have problems, follow the instructions in Troubleshoot Firefox issues caused by malware.

# Check if an extension is causing the problem

Firefox extensions could be causing the issue, especially the ones that have network access and/or those that rely on manipulating webpage content. Try disabling your extensions in the Add-ons Manager one by one and then reload the page. See Disable or remove Add-ons and Troubleshoot extensions, themes and hardware acceleration issues to solve common Firefox problems for more information.

***Based on information from Error loading websites (mozillaZine KB)***