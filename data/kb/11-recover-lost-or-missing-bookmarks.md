If your bookmarks have suddenly disappeared, don't worry - you should be able to recover them. This article explains how to get back your bookmarks if they disappeared unexpectedly.

The right recovery method depends on what happened. Firefox may be using a different profile, your bookmarks may still be available through Sync or Firefox may have a backup you can restore.

* If you are able to add, delete, and edit your bookmarks but the changes are lost when you restart Firefox, see Can't add, change or save bookmarks - How to fix.

# Find the likely cause

Start here and use the description that best matches what you see:

* **You see only Firefox's default bookmarks:** Firefox may have started with a different profile. Check whether another profile exists (Determine if Firefox has created a new profile).
* **Your bookmarks are missing after an update, reinstall, or Firefox Refresh:** Check for another profile and an Old Firefox Data folder, then try a bookmark backup.
* **Your bookmarks are missing on one device but still appear on another:** Check that you are signed in to the same Mozilla account and that Sync is enabled for bookmarks.
* **The Bookmarks Toolbar itself is missing:** Turn the Bookmarks Toolbar back on.
* **Your imported bookmarks are missing:** Look in the specially named folder created during the import.
* **You can see your bookmarks but cannot save changes:** See Can't add, change or save bookmarks - How to fix.

# I can see only the default set of bookmarks in the Bookmarks folder

Your bookmarks are associated with the Firefox profile you are using. There may be instances when you or Firefox creates a new profile containing the default set of bookmarks (for example, if you make a separate installation of Firefox or when you downgrade Firefox). A new profile may give you the impression that you have lost your bookmarks.

This can also happen after an update or reinstall if Firefox starts with a different profile than the one that contains your bookmarks.

## Determine if Firefox has created a new profile

To see if another profile exists, type **about:profiles** into the Firefox address bar and press the **[Windows / Linux]** Enter **[macOS]** Return  key. This will open the *About Profiles* page, which will list at least one profile and could list many. The profile that Firefox is currently using will show: **This is the profile in use and it cannot be deleted.** If you have another profile listed, you can launch that profile in a new Firefox browser window to see if it contains your lost bookmarks. See Recover user data missing after Firefox update or reinstall for more information.

If another profile contains your bookmarks, use that profile rather than restoring an older backup. Do not delete profiles until you have confirmed which one contains your data.

**[macOS]**

## Firefox creates a new profile each time it starts

A new profile is automatically created for each separate installation of Firefox (see Dedicated profiles per Firefox installation for details). If you are running Firefox directly from the disk image (`Firefox .dmg`) file you downloaded, it may be detected as a new installation each time you start Firefox. Do not run Firefox directly from the `.dmg` file; move it to the Applications folder instead. See How to download and install Firefox on Mac for instructions.

# My Bookmarks Toolbar is missing

If you were using the Bookmarks Toolbar for quick access to your favorite bookmarks and the toolbar is now missing, you may have turned off the option to display the Bookmarks Toolbar. To turn it back on:

**[Windows / Linux]**

* Right-click on an empty section of the navigation bar and select Bookmarks Toolbar in the pop-up menu.

**[macOS]**

* On the menu bar, click View, select Toolbars, and then select Bookmarks Toolbar.

For more information, see the Bookmarks Toolbar - Display your favorite websites at the top of the Firefox window article.

# I can't find all of my bookmarks and folders

You can view all of your bookmarks and folders when you click the Bookmarks menu item in the Firefox Menu bar**[Windows / Linux]** , if you enable the Menu bar .
You can also add a Bookmarks menu button to your Firefox toolbar, a button that with a click, shows all of your bookmarks and folders. Follow these steps:

1. Click the menu button , then click More tools and select Customize Toolbar…
2. Drag the Bookmarks Menu button  from the Customize Firefox tab onto the toolbar.

If you know a bookmark exists but cannot find it, open the Bookmarks menu and check the folders there. A bookmark that appears to be missing may have been moved into another folder rather than deleted.

# My bookmarks have disappeared

Firefox automatically backs up your bookmarks and saves up to 15 backups in the profile bookmarkbackups folder. To recover bookmarks that were previously saved in the Bookmarks menu or on the Bookmarks toolbar but are now missing, you can restore them from one of these backups:

1. Click the menu button  to open the menu panel.
   Click Bookmarks and then click the Manage bookmarks bar at the bottom.
2. In the Library window, click the **[macOS]**  **[Windows / Linux]** Import and Backup  button and then select Restore.
3. Select the backup you want to restore from the list of dated automatic backups.
   * You can also select Choose File… to restore bookmarks from a manual backup, if you created one.
4. After confirming your choice, the bookmarks from the backup you selected will be restored.

For more information, see Restore bookmarks from backup or move them to another computer.
Before restoring a backup, make sure the backup is newer than the last time you know your bookmarks were present but older than when they disappeared. Restoring a backup replaces the current bookmarks with the bookmarks from that backup.

## There is an "Old Firefox Data" folder on my desktop

In some cases, Firefox may create a folder on your desktop called "Old Firefox Data". This folder contains a complete backup of your Firefox profile and can be used to restore bookmarks and other missing information. If you have this folder on your desktop, see Restore bookmarks, passwords and data from an old Firefox profile.

Do not delete the Old Firefox Data folder until you have recovered the information you need.

**[Windows]**

# No bookmarks are visible after installing an add-on

If you have restarted Firefox after installing an add-on and your bookmarks are gone, it's possible that Firefox did not close properly before restarting itself. To recover your bookmarks, restart your computer.

# I can't find my bookmarks after importing them

If you imported your bookmarks from another browser, you can find them inside a specially-named folder, for example, **From Google Chrome** or **From Microsoft Edge** depending on the browser, in one of these locations:

* At the end of the Firefox Bookmarks Toolbar.
* At the bottom of the Bookmarks list accessible from the Bookmarks Menu  toolbar button.
* In the Bookmarks Library. To open the Bookmarks Library window: Click the menu button  to open the menu panel.
  Click Bookmarks and then click the Manage bookmarks bar at the bottom.

If your source bookmarks were stored in a hierarchy of folders, the folder structure is preserved inside the specially-named folder. If desired, you can move your imported bookmarks to other folders. See Bookmarks in Firefox to learn more about organizing your bookmarks.

# When bookmarks cannot be recovered

Firefox can recover bookmarks when they are still present in another profile, available through Sync or included in a bookmark backup. However, recovery may not be possible when:

* The bookmarks were deleted before any available automatic or manual backup was created or updated.
* The profile containing the bookmarks was permanently deleted and no backup of that profile exists.
* The bookmarks were never synchronized and are not present on another device or in another Firefox profile.
* All available bookmark backups were created after the bookmarks were deleted.

If you cannot find your bookmarks in another profile, through Sync, or in an available backup, Firefox may not have a copy from which to restore them.

**Before giving up, check for an Old Firefox Data folder or another device that still has the bookmarks.** If another device still contains them, make a backup before making further changes.

***Based on information from Lost bookmarks (mozillaZine KB)***