using System.Collections.Generic;
using UnityEngine;

namespace Refinery
{
    /// Loads a side-channel material LUT (object_id -> color_hex) and assigns
    /// URP/Lit materials to MeshRenderers in the scene by GameObject name match.
    /// See docs/analysis/2026-04-25-refinery-material-data-sources.md.
    public class RefineryMaterialApplier : MonoBehaviour
    {
        [Tooltip("object_material_lut.json produced by scripts/build_refinery_material_lut.py")]
        public TextAsset lutJson;

        [Tooltip("URP/Lit shader. Leave empty to auto-resolve.")]
        public Shader litShader;

        [Tooltip("Apply on Awake. Disable when driving from another script.")]
        public bool applyOnAwake = true;

        [Tooltip("Search included children only when assigning. Otherwise scans the whole scene.")]
        public bool restrictToChildren = false;

        readonly Dictionary<string, Material> _materialCache = new();
        Dictionary<string, LutEntry> _byObjectId;

        void Awake()
        {
            if (applyOnAwake) Apply();
        }

        public void Apply()
        {
            if (lutJson == null)
            {
                Debug.LogError("[RefineryMaterialApplier] lutJson not assigned");
                return;
            }
            var shader = litShader != null ? litShader : Shader.Find("Universal Render Pipeline/Lit");
            if (shader == null)
            {
                Debug.LogError("[RefineryMaterialApplier] URP/Lit shader not found. Assign litShader manually.");
                return;
            }

            var file = JsonUtility.FromJson<LutFile>(lutJson.text);
            if (file == null || file.entries == null)
            {
                Debug.LogError("[RefineryMaterialApplier] LUT parse failed");
                return;
            }

            _byObjectId = new Dictionary<string, LutEntry>(file.entries.Length);
            foreach (var e in file.entries) _byObjectId[e.object_id] = e;

            var renderers = restrictToChildren
                ? GetComponentsInChildren<MeshRenderer>(includeInactive: true)
                : FindObjectsByType<MeshRenderer>(FindObjectsInactive.Include, FindObjectsSortMode.None);

            int applied = 0, missed = 0;
            foreach (var r in renderers)
            {
                var entry = ResolveEntry(r.gameObject);
                if (entry == null) { missed++; continue; }
                r.sharedMaterial = GetOrCreateMaterial(shader, entry.color_hex);
                applied++;
            }
            Debug.Log($"[RefineryMaterialApplier] applied={applied} missed={missed} total_lut_entries={file.entries.Length}");
        }

        LutEntry ResolveEntry(GameObject go)
        {
            // Walk up parents — glTFast often nests the mesh node under an "untitled" root.
            var t = go.transform;
            while (t != null)
            {
                if (_byObjectId.TryGetValue(t.name, out var entry)) return entry;
                t = t.parent;
            }
            return null;
        }

        Material GetOrCreateMaterial(Shader shader, string hex)
        {
            if (_materialCache.TryGetValue(hex, out var cached)) return cached;
            var mat = new Material(shader) { name = $"Refinery_{hex}" };
            if (ColorUtility.TryParseHtmlString("#" + hex, out var col)) mat.color = col;
            else mat.color = Color.gray;
            _materialCache[hex] = mat;
            return mat;
        }

        [System.Serializable]
        public class LutFile
        {
            public string schema_version;
            public string subset_id;
            public string palette_version;
            public LutEntry[] entries;
        }

        [System.Serializable]
        public class LutEntry
        {
            public string object_id;
            public string material;
            public string domain;
            public string applied_key;
            public string color_hex;
            public string source;
            public string system_path;
            public string name;
            public string category;
        }
    }
}
