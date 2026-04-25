# Coplay MCP Setup (D12)

**Date**: 2026-04-25
**Task**: D12 / Phase 3 (Unity automation bridge)
**Commit**: TBD

---

## 1. Language / Content

| Language | File | Purpose |
|----------|------|---------|
| Markdown | `docs/PROJECT-JOURNAL.md` | D12 entry, Q2/Q7 status, External Dependencies refresh |
| JSON | `unity/Packages/manifest.json` | Removed `com.coplaydev.coplay`; added `com.coplaydev.unity-mcp` |
| JSON | `unity/Packages/packages-lock.json` | Pinned MCP for Unity at commit `9daf4fc33c33` |
| (filesystem) | `unity/Packages/Coplay/` | Removed orphan Plugin runtime data |
| Markdown | `docs/tasklog/2026-04-25-coplay-mcp-setup.md` | This log |

## 2. Problem

The next milestone after the refinery material side-channel pipeline is
schedule visibility playback. Driving Unity Editor from Claude Code
requires an MCP bridge. Two CoplayDev products were available:

- Coplay Unity Plugin (in-Editor chat UI, closed-source DLL,
  Coplay-billed)
- MCP for Unity (open-source standalone bridge)

Initial setup installed the Plugin first, then ran into:

1. The Plugin's auto-configuration assumed Claude Code was on Windows;
   it could not register the WSL-side `claude` CLI.
2. Plugin LLM usage runs through Coplay's billing, parallel to the
   developer's Claude Code Max plan — duplicate cost and no benefit
   from existing Anthropic context (skills, project memory, CLAUDE.md).
3. The Plugin Setup Wizard's "HTTP local" mode bound the server to
   `127.0.0.1` only, which was unreachable from WSL under the project's
   default `localhostForwarding=true` (NAT) WSL2 networking mode.
4. Switching to "HTTP remote" was a UI trap: it asked for an external
   server URL + API key (the paid hosted Coplay MCP), not a `0.0.0.0`
   bind option for the local server.
5. WSL2 mirrored networking would have solved (3) but required a
   shutdown that interrupted the active Claude Code session.

## 3. Analysis

- The Plugin and MCP for Unity are layered, not competing. Plugin =
  in-Editor chat. MCP for Unity = programmatic bridge for external
  clients. Only the MCP is needed when Claude Code is the client.
- DLL inspection of the Plugin showed `Editor/Unity-v6000.3/Coplay-v8.17.1.dll`
  + `Unity-v2022.3/Coplay-v8.17.1.dll` (closed source, no `.cs`); no
  refactoring of the Plugin itself was possible without source access.
- MCP for Unity ships a Python server packaged at `mcpforunityserver`
  (PyPI/uv); the Unity package compiles `MCPForUnity.Editor.dll` into
  the Unity project's `Library/ScriptAssemblies/` and registers a
  TCP socket on default port `6400` once the Editor's MCP for Unity
  Window is opened (`Window > MCP For Unity > Toggle MCP Window`,
  shortcut `Ctrl+Shift+M`).
- `claude mcp add` accepts a Windows `.exe` path through WSL's Win32
  interop. Spawning `uvx` from WSL bash via `/mnt/c/Users/x8333/anaconda3/Scripts/uvx.exe`
  starts the Python MCP server on Windows where Unity is running, and
  pipes stdin/stdout back to Claude Code. This sidesteps both the
  HTTP-binding question and the WSL2 networking question.

## 4. Solution

Adopted Option B from the Coplay product comparison, recorded as D12:

1. Removed Coplay Plugin via Unity Package Manager. Cleaned up the
   orphan runtime data folder `unity/Packages/Coplay/`.
2. Installed `com.coplaydev.unity-mcp` (commit `9daf4fc33c33`,
   declared as `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main`)
   via Unity Package Manager.
3. Installed `uv`/`uvx` on Windows (Anaconda's
   `C:\Users\x8333\anaconda3\Scripts\uvx.exe`, version `0.9.7`).
4. Registered the bridge with Claude Code from WSL:

   ```bash
   claude mcp add --scope local --transport stdio UnityMCP -- \
     /mnt/c/Users/x8333/anaconda3/Scripts/uvx.exe \
     --offline --from "mcpforunityserver==9.6.6" mcp-for-unity
   ```

   Stored in `~/.claude.json` (WSL home), keyed by project working
   directory. Not committed.
5. In Unity, opened the MCP for Unity Window and clicked the
   Connection-section Start button (next to "Unity Socket Port"), not
   the Local-Server Start button. Bridge began listening on
   `127.0.0.1:6400`.
6. Verified end-to-end: `claude mcp list` showed `UnityMCP — ✓ Connected`;
   `manage_scene get_active` returned the active scene; `find_gameobjects`
   located both the `_RefineryMaterials` controller and
   `02b874b7-...` GLB instance from the MVP subset.

Side discovery: Unity Hub silently auto-upgraded the project's Editor
from `6000.3.4f1` to `6000.4.4f1`. ProjectVersion.txt now reflects the
new pin; both Coplay packages declare `unity: 2021.3` minimum so no
incompatibility arose.

## 5. Result

- Unity socket bridge listening on `127.0.0.1:6400` (Unity Editor
  PID at the time of setup: 45868).
- Claude Code MCP server registered; tool calls (manage_scene,
  read_console, find_gameobjects) verified.
- Q2 resolved (MCP for Unity standalone chosen).
- Q7 status updated to reflect Unity `6000.4.4f1` pin.
- D12 recorded.
- External Dependencies updated:
  - `Coplay Unity Plugin`: Rejected (D12).
  - `CoplayDev Unity MCP`: Resolved; pinned at v9.6.6 / commit `9daf4fc33c33`.

Unresolved / deferred:
- WSL2 mirrored networking is still off; if a future workflow needs
  HTTP transport, that becomes the better path. Current stdio +
  Win32 interop is sufficient for solo work.
- The Plugin's `SkillSync` left auto-generated skills under
  `C:\Users\x8333\.claude\skills\unity-mcp-skill`. These are
  Windows-side and not loaded by the WSL Claude Code session;
  intentionally ignored.

Commit: TBD.
