Enhanced Tracking Protection in Firefox automatically protects your privacy as you browse. It blocks many types of hidden scripts and trackers that follow you around online to collect information about your browsing habits and interests without breaking site functionality. It also includes protections against harmful scripts, such as malware that drains your battery.

# Protections Dashboard

To see what’s been blocked on all sites over the past week, visit your Protections Dashboard. Click the shield  to the left of the address bar and select Protections Dashboard or type Type  **about:protections** into the address bar. This will open the *Protections Dashboard* page in a new tab.

# What Enhanced Tracking Protection blocks

Firefox relies on a list of known trackers provided by Disconnect. By default, Firefox blocks these types of trackers and scripts:

* Social media trackers
* Cross-site tracking cookies
* Fingerprinters
* Cryptominers
* Tracking content: These trackers are hidden in ads, videos and other in-page content. In **Standard** mode, tracking content is blocked only in Private Windows. To add this protection to all windows, visit your privacy preferences and select **Strict** or **Custom** as explained below.

**Note:** Total Cookie Protection is enabled by default in Standard mode. This confines every cookie to the website where it was created and prevents cookies from tracking you across sites (to learn more, see Introducing Total Cookie Protection in Standard Mode). Strict Mode also includes Enhanced Cookie Clearing, which allows users to clear third-party cookies more effectively.

To learn more about trackers and scripts blocked by Firefox, see Trackers and scripts Firefox blocks in Enhanced Tracking Protection, Third-party trackers and SmartBlock for Enhanced Tracking Protection.

# Bounce Tracking Protection

Bounce Tracking Protection is a feature in Enhanced Tracking Protection (ETP) strict mode that prevents redirect trackers (bounce trackers) from collecting data as you navigate between websites. These trackers redirect you through intermediate URLs to gather information about your browsing habits.

How it works:

* Firefox automatically detects and classifies bounce trackers.
* Cookies and storage associated with these trackers are cleared if no user interaction occurs within a designated time.

Bounce Tracking Protection effortlessly enhances your privacy, operating in the background when ETP is set to strict mode. For technical details, visit the Mozilla Source Docs.

# How to tell when Firefox is protecting you

The shield to the left of the address bar tells you if Firefox is blocking trackers and scripts on a site.

* **Blocking:** Firefox **blocked** trackers and harmful scripts on a site. Open the shield to see what was blocked.The icon also means Enhanced Tracking Protection is turned on on a site.

* **Active:** Enhanced Tracking Protection is turned **on** on a site, but Firefox **didn't block** any trackers or scripts.

* **Inactive:** Enhanced Tracking Protection is turned **off** on a site. Open the shield and toggle the switch to turn it back on.

The shield icon to the left of the address bar shows when Firefox is protecting you from trackers and other harmful content.

* **Blocking:** Enhanced Tracking Protection is turned on for the site. If the shield icon appears without a number, Firefox didn't find any trackers to block. If a number appears next to the shield, Firefox found and blocked trackers. The number shows how many trackers were blocked on the page. Select the shield icon to see more details in the Privacy Panel.
* **Inactive:** Enhanced Tracking Protection is turned **off** on a site. Open the shield and toggle the switch to turn it back on.

## Shield animation feature

This feature is experimental and is being introduced to the Firefox user base through a progressive rollout. It may not yet be available to all users. Additionally, remote improvements must be enabled.

The first time you visit a website during a browsing session, if Firefox blocks trackers on that site, the shield icon briefly animates and expands to show the number of trackers blocked. When the animation ends, the shield returns to its normal size and the number of blocked trackers remains visible next to it.

The animation appears only once per website during each browsing session. If you visit the website again during the same session, you'll see the shield icon with the number of trackers blocked, but the animation won't appear again.

You can select the shield icon at any time to open the Privacy Panel and see more information about the trackers Firefox blocked. The number shown next to the shield matches the number of blocked trackers shown in the Privacy Panel.

If you prefer not to see the animation, you can turn it off:

1. **[macOS]** In the Menu bar at the top of the screen, click Firefox and select Settings (or Preferences, in some cases). **[Windows / Linux]** Click the menu button  and select Settings.
2. Select Privacy and security on the left.
3. Under the *Enhanced Tracking Protection* section, clear the checkbox next to **Show trackers blocked in address bar**.

**Note:** Turning off **Show trackers blocked in address bar** disables the shield animation and hides the blocked tracker count next to the shield. Enhanced Tracking Protection will continue to block trackers, and you can still select the shield icon to see the number of trackers blocked in the Privacy Panel.

# How to tell what’s being blocked on a site

Click the shield icon to see what Firefox has blocked.

1. Click the shield icon to access the Unified Trust panel.
2. Click the See All button to see what Firefox has blocked.

This panel will display different information depending on the site you’re on.

* **Blocked:** Firefox blocked these trackers and scripts. Select each one to see a detailed list.
* **Allowed:** These are the trackers and scripts that were allowed to load on the page. This happens because some websites may require loading trackers and scripts to function properly. Firefox only allows trackers and scripts needed for the site to work and blocks the rest. For more information, visit SmartBlock for Enhanced Tracking Protection.
* **None Detected:** Firefox looked for these trackers and scripts, but did not find them on this site.

* Select Protection settings to adjust your global privacy settings.
* Select Protections dashboard to view a personalized summary of your protections over the past week, including tools to take control of your online security.

# What to do if a site seems broken

If a site seems broken, disabling Enhanced Tracking Protection might fix the issue by allowing trackers on just that site. Enhanced Tracking Protection will still prevent trackers on other sites. To disable it:

1. Visit the website.
2. At the left of the address bar, click the    shield icon.
3. At the top the bottom  of the panel, toggle off the Enhanced Tracking Protection switch . The site will be added to your Enhanced Tracking Protection exception list, allowing trackers on it, and the page will reload automatically.

Follow the same process to turn Enhanced Tracking Protection back on. The site will be removed from the exception list, and the page will reload automatically.

You may encounter breakage on some sites when you’re in **Strict** Enhanced Tracking Protection. This is because trackers are hidden in some content. For example, a website might embed an outside video or social media post that contains trackers. To block the trackers, Firefox must also block the content itself. Trackers are often hidden in the following types of content:

* Login fields
* Forms
* Payments
* Comments
* Videos

## Report a broken site

If disabling Enhanced Tracking Protection resolves issues with a broken site, consider submitting a *Broken Site* report to the Webcompat team. To do so, open the *Report broken site* panel:

1. Click the menu  button and select Report Broken Site at the bottom , click Help and Report at the bottom and select Report Broken Site .
   Alternatively, click the  shield icon at the left of the address bar and select Report broken site.
2. The URL field will show up with the current tab URL; you can change it if you wish.
3. Pick an option from the *What's broken* dropdown under *What's not working?*  and follow the prompts to complete and send the report.

For more information, see How do I report a broken site in Firefox desktop?

# Adjust your global Enhanced Tracking Protection settings

When you download Firefox, all protections included in **Standard** Enhanced Tracking Protection are already enabled.

To view or change your Enhanced Tracking Protection settings for all sites, follow the steps below.

1. On the left side of your address bar on any website, click the shield    icon.
2. Select Protection Settings Privacy Settings .
3. This will open the Settings *Privacy & Security* *Privacy and security*  page in a new tab and show you the **Enhanced Tracking Protection** settings.

   To change settings, click Advanced settings.

**Tip:** These settings are also available from the Firefox menu:
**[macOS]** In the Menu bar at the top of the screen, click Firefox and select Settings (or Preferences, in some cases). **[Windows / Linux]** Click the menu button  and select Settings.
Then select Privacy & Security Privacy and security .

## Standard Enhanced Tracking Protection

By default, Firefox blocks the following on all sites:

* Social media trackers
* Cross-site tracking cookies (other third-party cookies are isolated)
* Tracking content in Private Windows only
* Cryptominers
* Fingerprinters

## Strict Enhanced Tracking Protection

To further increase privacy, select **Strict** Enhanced Tracking Protection. This will block the following:

* Social media trackers
* All cross-site cookies
* Tracking content in all windows
* Cryptominers
* Fingerprinters

To select this setup for your Enhanced Tracking Protection settings, follow these steps:

1. Click the shield    to the left of the address bar on any webpage.
2. Click Protection Settings Privacy Settings .
   * The Firefox Settings
     Privacy & Security Privacy and security  page will open.
3. Under *Enhanced Tracking Protection*, click Advanced settings and select **Strict**.
4. Select the  button to apply your new privacy settings.

## Custom Enhanced Tracking Protection

Want to block some trackers and scripts, but not others? Use **Custom** Enhanced Tracking Protection.

1. Click the shield    to the left of the address bar on any webpage.
2. Click Protection Settings Privacy Settings .
   * The Firefox Settings
     Privacy & Security Privacy and security  page will open.
3. Under *Enhanced Tracking Protection*, click Advanced settings and select **Custom**.
4. Choose which trackers and scripts to block by selecting those checkboxes.
5. Select the  button to apply your new privacy settings.

You can also turn off all protections in **Custom** by deselecting all checkboxes. This allows all trackers and scripts to load.

### WebCompat exception checkboxes

Starting with Firefox version 142, Firefox may allow certain trackers to load on specific websites to ensure they work properly. These are called **WebCompat exceptions**, and you can manage them in Strict and Custom settings. To learn more, see Manage Enhanced Tracking Protection exceptions.

* In the **Strict** and **Custom** sections, select or deselect the checkboxes to adjust Web compatibility exceptions.
* Deselecting these options will block **all** trackers, even on sites that may break without them.

**Note:** Disabling WebCompat exceptions can improve privacy, but may cause website features (like video playback or login popups) to stop working correctly.

To apply changes, click the  if prompted.

# Copy Clean Link

The *Copy Clean Link* feature is automatically enabled to safeguard users against URL-based tracking by stripping tracking parameters from any copied URL.

## Copy from the address bar

To copy a URL from the address bar by stripping any tracking parameters it may have, do the following:

1. **[Windows / Linux]** Right-click **[macOS]** Right-click (or hold down the Control key while you click)
   the URL you want to copy and select Copy Clean Link.
2. Paste the clean URL from the clipboard.

## Copy from in-page links

To copy URLs from in-page links by stripping any tracking parameters they may have, do the following:

1. **[Windows / Linux]** Right-click **[macOS]** Right-click (or hold down the Control key while you click)
   the URL you want to copy and select Copy Clean Link.
2. Paste the clean URL from the clipboard.