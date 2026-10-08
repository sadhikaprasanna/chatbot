When you run Firefox in **Troubleshoot Mode**, add-ons and some other features and customizations are disabled (see below for details). If you're having a problem in Firefox that does not occur in Troubleshoot Mode, the cause of the problem is one of the disabled items.

**Note:** Troubleshoot Mode was previously known as *Safe Mode* in earlier versions of Firefox.

# Start Firefox in Troubleshoot Mode

Click the menu button , click Help Help and Report , select Troubleshoot Mode… and click Restart in the *Restart Firefox in Troubleshoot Mode?* dialog.

**Note:** You can also start Firefox in Troubleshoot Mode by **[Windows]** holding down the Shift key while starting Firefox. **[macOS]** holding down the option key while starting Firefox. **[Linux]** quitting Firefox and then going to your **Terminal** and running: `firefox -safe-mode`
You may need to specify the Firefox installation path (for example /usr/lib/firefox).

# Troubleshoot Mode window

Choose one of these options:

* Click Open to start Firefox with a default theme, your extensions disabled and some other features and customizations turned off. These changes are temporary. When you leave Troubleshoot Mode and start Firefox normally, your add-ons and other settings will return to the state they were in before you entered Troubleshoot Mode.
* Click Refresh Firefox to restore Firefox to its factory default state while saving your essential information. These changes are permanent. Before you choose this option, see Refresh Firefox - reset add-ons and settings for more information.

# Diagnose problems in Troubleshoot Mode

After you start Firefox in *Troubleshoot Mode*, test its behavior and see if the problem goes away.

## The problem happens in Troubleshoot Mode

If the problem still happens in Troubleshoot Mode, it is not being caused by an add-on or by one of the other features and customizations that Troubleshoot Mode disables. Other possible causes include changes made to Firefox preference settings, which are not disabled in Troubleshoot Mode. See the following articles for solutions:

* Troubleshoot and diagnose Firefox problems
* Reset Firefox preferences to troubleshoot and fix problems

## The problem does not happen in Troubleshoot Mode

If the problem does not happen in Troubleshoot Mode, the most likely cause is an extension, theme or hardware acceleration. See Troubleshoot extensions, themes and hardware acceleration issues to solve common Firefox problems for solutions.

# Exit Troubleshoot Mode

1. **[Windows]** Click the Firefox menu  and select Exit. **[macOS]** Click the Firefox menu at the top of the screen and select Quit Firefox. **[Linux]** Click the Firefox menu  and select Quit.
2. Start Firefox as you normally would.

   **Note:** If Firefox keeps starting in Troubleshoot Mode, see Firefox is stuck in Troubleshoot Mode.

# What does Troubleshoot Mode disable?

* Add-ons (extensions and themes)
* Hardware acceleration and WebGL
* Window and sidebar size and position settings
* userChrome and userContent customizations
* JavaScript Just-in-time (JIT) compiler

***Based on information from Safe mode (mozillaZine KB)***