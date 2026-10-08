At times, Firefox may require significant system resources to download, process, and display web content. We know it’s frustrating when Firefox slows down, especially if it interrupts your work or browsing. If you are experiencing periods of sustained high resource usage while using Firefox, this article presents some options for you to review.

* The CPU (Central Processing Unit) is the "brain" of the computer.
* The RAM (Random Access Memory) or Memory helps your computer perform multiple tasks at the same time.
* When your system resources are being heavily used, the overall performance and stability of the computer can be impacted.
* Depending on your operating system, you can review and monitor resource usage through specific tools. See the Use additional troubleshooting tools section below for more information.

**Note:** If you send performance data, Mozilla will gather data including memory and CPU usage, which will help make Firefox better for future versions.

# Update to the latest version

The latest Firefox version may include performance improvements. Update Firefox to the latest release.

# Check for problematic extensions and themes

Extensions and themes can cause Firefox to use more system resources than it normally would.

To determine if an extension or theme is causing Firefox to use too many resources, start Firefox in Troubleshoot Mode and observe its memory and CPU usage. In Troubleshoot Mode, extensions and themes are disabled, so if you notice a significant improvement, you can try disabling or uninstalling extensions.

* For more information on starting Firefox in Troubleshoot Mode and on how to find which extension or theme is causing your problem, see Troubleshoot extensions, themes and hardware acceleration issues to solve common Firefox problems.

# Hide intrusive content

Many web pages have content you don't need, but which still use system resources to display its content. Firefox's built-in content blocking can help save resources by preventing third-party tracking content from loading. See Enhanced Tracking Protection for details.

Some extensions allow you to block unnecessary content; for example:

* Adblock Plus and uBlock Origin allow you to hide ads on websites.
* NoScript allows you to selectively enable and disable scripts running on websites.

Please reach out to the add-on developer directly, if you need help with a specific add-on.

# Use fewer tabs

Each tab requires Firefox to store a web page in memory. If you frequently have **more than 100 tabs open**, consider using a more lightweight mechanism to keep track of pages to read and things to do, such as:

* Bookmarks. *Hint: "Bookmark All Tabs" will bookmark a set of tabs.*
* To-do list applications.

# Close tabs that use too many system resources

Some websites use scripts that use a lot of memory and/or CPU to keep them up to date, such as online mail client pages. If these scripts are not optimized, they can lead to the use of too many system resources. You can see which tabs are using the most system resources by opening the Firefox Task Manager (*about:processes* page). If you do not need these tabs open all the time, you can close them to reduce system resources usage.

# Check Firefox hardware acceleration

Firefox hardware acceleration eases memory and CPU usage in many cases.
Check in Firefox's performance settings that hardware acceleration is turned on. Also make sure that your graphics drivers are up-to-date.

# Close other applications

Having many applications running simultaneously may cause your computer to run slowly and other applications to do so as well. By closing down some of the unnecessary applications, system usage will be reduced.

# Delete content-prefs.sqlite file

Firefox stores your data in various files in your profile folder. The file used for saving individual website settings might be corrupt. If you delete (or rename) that file, your zoom level settings will be reset but it could decrease CPU usage.

1. * **[Windows / Linux]** Click the menu button , click Help Help and Report  and select More Troubleshooting Information. **[macOS]** From the Help menu, select More Troubleshooting Information.  The **Troubleshooting Information** tab will open.
   * Under the **Application Basics** section next to *Profile Folder **[Linux]** Profile Directory* , click **[Windows]** Open Folder **[macOS]** Show in Finder **[Linux]** Open Directory . **[macOS]** A window will open that contains your profile folder. **[Windows]** Your profile folder will open. **[Linux]** Your profile directory will open.

   **Note:** If Firefox displays an error after clicking Open Folder or if  you are unable to open or use Firefox, follow the instructions in Finding your profile without opening Firefox.
2. **[Windows]** Click the Firefox menu  and select Exit. **[macOS]** Click the Firefox menu at the top of the screen and select Quit Firefox. **[Linux]** Click the Firefox menu  and select Quit.
3. In your profile folder, delete the file content-prefs.sqlite. It will be recreated next time you open Firefox.

# Refresh Firefox

The *Refresh Firefox* feature can fix many issues by restoring your Firefox profile to its default state while saving your essential information.
See Refresh Firefox - reset add-ons and settings for details.

# Use additional troubleshooting tools

There are a variety of troubleshooting tools that can be used both in Firefox and on your operating system to troubleshoot elevated system resource usage.

## Firefox tools

* The Firefox Task Manager (not to be confused with Windows Task Manager) is a great tool to see whether tabs and extensions are using too many system resources.
* The **about:memory** page allows you to troubleshoot specific issues relating to memory (for instance, caused by a website, an extension, a theme, etc.) and sometimes its Minimize memory usage button may help you instantly reduce memory usage. For guidance on use of **about:memory** visit about:memory.
* Even if you're not a programmer, you can try your hand at some other tools and tips Firefox developers use to debug leaks.

## Operating system tools

**[Windows]**

* View how system resources are being used by checking the Windows Task Manager *Performance* tab (click on "More details" in the Task Manager to show all tabs) . See this Windows blog post at Microsoft's site for more information.

**[macOS]**

* View how system resources are being used by checking Activity Monitor. See How to use Activity Monitor on your Mac at Apple's site for more information.

**[Linux]**

* Although it's not included on every distribution of Linux, most versions of Linux have a graphical resource monitor. It's often called System Monitor, but there are other alternatives also available.
* Running the `top` command in the terminal will display a list of all the running processes and their system resource consumption.

**WARNING:** There are a variety of third-party programs that promise to increase your computer's performance. You should exercise caution when installing third-party software and only use reputable software provided by an official source.

# Restart Firefox

Firefox may use more system resources if it's left open for long periods of time. A workaround for this is to periodically restart Firefox. You can configure Firefox to save your tabs and windows so that when you start it again, you can start where you left off. See Restore previous session - Configure when Firefox shows your most recent tabs and windows for details.

# Restart your computer

Firefox may grind to a halt due to operating system issues, such as a pending Windows update,  that can be resolved by restarting your computer.

# Address hardware-related performance issues

If you've tried all the above and your memory usage is still close to the maximum, maybe it's time for you to add more memory to your computer. Adding RAM will provide a huge performance boost.

Alternatively, it may be time to upgrade your computer. As technology progresses, software is becoming more advanced and requires more powerful computers to run effectively.