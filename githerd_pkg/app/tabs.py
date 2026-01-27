# -*- coding: utf-8 -*-
"""
GitHerd — App tabs mixin.

Handles tab management, switching, and colors.
"""

from pathlib import Path
import customtkinter as ctk

from ..config import (
    load_global_settings, save_global_settings, load_repo_config,
    save_repo_config
)
from ..git_utils import is_git_repo, detect_repo_settings
from ..widgets import TabButton
from ..repo_tab import RepoTabContent


class AppTabsMixin:
    """Mixin for tab management."""

    def get_tab_bg_state(self, tab):
        """Return background state for tab."""
        if not tab.git_healthy:
            return "red"
        if tab.pending_branches and not tab.polling:
            return "red"
        if tab.polling:
            return "green"
        return "default"

    def update_tab_color(self, tab):
        """Update tab button color."""
        tab_name = tab.tab_name
        if tab_name not in self.tab_buttons:
            return

        btn = self.tab_buttons[tab_name]
        bg_state = self.get_tab_bg_state(tab)

        # Define colors
        if bg_state == "green":
            fg_color = "#2d5a2d"
            hover_color = "#3d7a3d"
        elif bg_state == "red":
            fg_color = "#8b2020"
            hover_color = "#ab3030"
        else:
            fg_color = "#3d3d3d"
            hover_color = "#4a4a4a"

        # Update button colors
        btn.configure(fg_color=fg_color, hover_color=hover_color)

        # Update indicator
        if tab.syncing:
            btn.set_indicator("⭯")
        elif tab.has_update:
            btn.set_indicator("●")
        else:
            btn.set_indicator("")

        self.update_title()

    def mark_tab_updated(self, tab):
        """Mark tab as having an update."""
        if not tab.has_update:
            tab.has_update = True
            self.update_tab_color(tab)

    def clear_tab_marker(self, tab):
        """Clear update marker from tab."""
        if tab.has_update:
            tab.has_update = False
            self.update_tab_color(tab)

    def add_repo(self, repo_path, switch_to=True):
        """Add a repository tab."""
        repo_name = Path(repo_path).name

        # Handle duplicate names
        tab_name = repo_name
        counter = 1
        while tab_name in self.tabs:
            counter += 1
            tab_name = f"{repo_name} ({counter})"

        # Create tab button with custom indicator overlay
        btn = TabButton(
            self.tab_bar,
            text=repo_name,
            fg_color="#3d3d3d",
            hover_color="#4a4a4a",
            corner_radius=8,
            height=32,
            command=lambda n=tab_name: self.on_tab_click(n)
        )
        btn.pack(side="left", padx=(0, 8), pady=8)
        # Double-click for sync now (advanced mode)
        btn.bind("<Double-Button-1>", lambda e, n=tab_name: self.on_tab_double_click(n))
        self.tab_buttons[tab_name] = btn

        # Create content directly in container
        tab_content = RepoTabContent(self.content_container, repo_path, self, tab_name)
        self.tab_frames[tab_name] = tab_content

        self.tabs[tab_name] = tab_content
        self.tab_paths[tab_name] = repo_path

        # Switch to new tab if requested
        if switch_to:
            self.switch_tab(tab_name)
        self.after(100, self.update_title)

        # Auto-start polling if enabled AND restore_polling disabled
        if self.global_settings.get("auto_start_polling", False) and not self.global_settings.get("restore_polling", False):
            self.after(500, tab_content.toggle_polling)

    def on_tab_click(self, tab_name):
        """Handle tab click - switch or toggle polling in advanced mode."""
        if self.global_settings.get("advanced_mode", False):
            # Advanced mode: wait to distinguish single/double click
            if hasattr(self, '_click_timer') and self._click_timer:
                self.after_cancel(self._click_timer)
                self._click_timer = None

            def do_single_click():
                self._click_timer = None
                if self.current_tab == tab_name:
                    # Already selected -> toggle polling
                    tab = self.tabs.get(tab_name)
                    if tab and tab.git_healthy:
                        tab.toggle_polling()
                else:
                    # Not selected -> switch
                    self.switch_tab(tab_name)

            self._click_timer = self.after(300, do_single_click)
            self._click_tab = tab_name
        else:
            # Normal mode: immediate switch
            self.switch_tab(tab_name)

    def on_tab_double_click(self, tab_name):
        """Handle tab double-click - sync now in advanced mode."""
        if self.global_settings.get("advanced_mode", False):
            # Cancel single click timer
            if hasattr(self, '_click_timer') and self._click_timer:
                self.after_cancel(self._click_timer)
                self._click_timer = None

            tab = self.tabs.get(tab_name)
            if tab and tab.git_healthy:
                tab.manual_sync()

    def switch_tab(self, tab_name):
        """Switch to specified tab."""
        if tab_name not in self.tabs:
            return

        # Hide current tab
        if self.current_tab and self.current_tab in self.tab_frames:
            self.tab_frames[self.current_tab].pack_forget()
            # Reset previous button border
            if self.current_tab in self.tab_buttons:
                self.tab_buttons[self.current_tab].configure(border_width=0)

        # Show new tab
        self.tab_frames[tab_name].pack(fill="both", expand=True)
        self.current_tab = tab_name

        # Highlight active button with subtle border
        self.tab_buttons[tab_name].configure(border_width=1, border_color="#888888")

        # Mark as read
        tab = self.tabs[tab_name]
        if tab.has_update:
            tab.has_update = False
            self.update_tab_color(tab)

        # Update Repository menu for new tab
        self.update_repo_menu()

    def close_tab(self, tab_name):
        """Close a repository tab."""
        if tab_name in self.tabs:
            tab = self.tabs[tab_name]
            # Stop polling properly
            if tab.polling:
                tab.polling = False
                tab.stop_event.set()
            tab.stop_countdown()
            # Wait for thread (max 5s)
            tab.wait_for_polling_thread(timeout=5)

            # Remove button
            if tab_name in self.tab_buttons:
                self.tab_buttons[tab_name].destroy()
                del self.tab_buttons[tab_name]

            # Remove content
            if tab_name in self.tab_frames:
                del self.tab_frames[tab_name]

            # Destroy tab content widget
            tab.destroy()
            del self.tabs[tab_name]
            del self.tab_paths[tab_name]

            # Switch to another tab if needed
            if self.current_tab == tab_name:
                self.current_tab = None
                if self.tabs:
                    first_tab = list(self.tabs.keys())[0]
                    self.switch_tab(first_tab)

            self.save_current_repos()
            self.update_title()

    def close_current_tab(self):
        """Close current repository tab."""
        if not self.tabs or not self.current_tab:
            return
        self.close_tab(self.current_tab)
