# SPDX-FileCopyrightText: Copyright (c) 2022-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from urllib.parse import unquote

import carb
import carb.settings
import omni.ui as ui
import requests
import toml
from omni.kit.browser.folder.core import FileDetailItem
from omni.kit.notification_manager import post_notification

from .style import CONTEXT_MENU_STYLE


def get_content_folder():
    try:
        global_config_path = carb.tokens.get_tokens_interface().resolve("${omni_global_config}")
        omniverse_config_path = os.path.join(global_config_path, "omniverse.toml").replace("\\", "/")
        contents = toml.load(omniverse_config_path)
        return contents.get("paths").get("content_root")
    except:
        return None


class ContextMenu(ui.Menu):
    """
    Context menu for asset browser.
    """

    def __init__(self):
        super().__init__("Asset browser context menu", style=CONTEXT_MENU_STYLE)
        self.url = None
        self._settings = carb.settings.get_settings()

        has_collect = False
        try:
            # pylint: disable=redefined-outer-name
            import omni.kit.tool.collect  # noqa: F401

            has_collect = True
            with self:
                ui.MenuItem(
                    f"{omni.kit.ui.get_custom_glyph_code('${glyphs}/none.svg')}  Collect", triggered_fn=self._collect
                )
        except ImportError:
            carb.log_warn("Plese enable omni.kit.tool.collect first to collect.")

        has_stage = False
        try:
            # pylint: disable=redefined-outer-name
            import omni.kit.menu.stage  # noqa: F401

            has_stage = True
            with self:
                if has_collect:
                    ui.Separator()

                ui.MenuItem(
                    f"{omni.kit.ui.get_custom_glyph_code('${glyphs}/plus.svg')}   Add at Current Selection",
                    triggered_fn=self.__add_at_current_selection,
                )
                ui.MenuItem(
                    f"{omni.kit.ui.get_custom_glyph_code('${glyphs}/plus.svg')}   Replace Current Selection",
                    triggered_fn=self.__replace_current_selection,
                )
                ui.Separator()
                ui.MenuItem(
                    f"{omni.kit.ui.get_custom_glyph_code('${glyphs}/cloud_download.svg')}  Download",
                    triggered_fn=lambda: self.__download_item(self.url),
                )

        except ImportError:
            carb.log_warn("Plese enable omni.kit.menu.stage first to use add or replace at current selection.")

        with self:
            try:
                import omni.kit.clipboard

                if has_collect or has_stage:
                    ui.Separator()
                ui.MenuItem(
                    f"{omni.kit.ui.get_custom_glyph_code('${glyphs}/share.svg')}  Copy URL Link",
                    triggered_fn=self.__copy_url_link,
                )
            except ImportError:
                carb.log_warn("Plese enable omni.kit.clipboard first to copy URL link.")

    def _collect(self):
        try:
            # pylint: disable=redefined-outer-name
            import omni.kit.tool.collect

            collect_instance = omni.kit.tool.collect.get_instance()
            collect_instance.collect(self.url)

            # change the collect target folder to content folder that in launcher's setting
            folder = get_content_folder()
            if folder:
                stage_name = os.path.splitext(os.path.basename(self.url))[0]
                if not folder.endswith("/"):
                    folder += "/"
                folder = omni.client.normalize_url(folder)

                # Hard-decoding url currently since combine_urls will encode url
                folder = unquote(folder)

                folder.replace("\\", "/")
                collect_instance._main_window.show(f"{folder}Collected_{stage_name}")
            else:
                carb.log_warn("Failed to get the content folder set in launcher.")

            collect_instance = None
        except ImportError:
            carb.log_warn("Failed to import collect module (omni.kit.tool.collect). Please enable it first.")
        except AttributeError:
            carb.log_warn("Require omni.kit.tool.collect v2.0.5 or later!")

    def __add_at_current_selection(self):
        try:
            # pylint: disable=redefined-outer-name
            from omni.kit.menu.stage.content_browser_options import ContentBrowserOptions

            ContentBrowserOptions._add_file_to_stage(self.url, self._settings, False)
        except Exception:
            pass

    def __replace_current_selection(self):
        try:
            # pylint: disable=redefined-outer-name
            from omni.kit.menu.stage.content_browser_options import ContentBrowserOptions

            ContentBrowserOptions._add_file_to_stage(self.url, self._settings, True)
        except Exception:
            pass

    def __copy_url_link(self):
        import omni.kit.clipboard

        omni.kit.clipboard.copy(self.url)

    def __download_item(self, url):
        filename = os.path.basename(url)

        # download file to users Download folder
        download_folder = os.path.expanduser("~") + "/Downloads/"
        download_path = download_folder + filename

        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(download_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            post_notification(f"Downloaded {filename} to {download_path}")
        except requests.exceptions.RequestException as e:
            post_notification(f"Failed to download {filename}: {e}")
