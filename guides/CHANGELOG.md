# Guides Directory Changelog

## 2026-03-19 - Shared Optimizations Extraction

### Added
- **SHARED_OPTIMIZATIONS.md:** New centralized document for battery limits, Wi-Fi powersave, audio presets, NPU status, VA-API, verification checklist, and Thai font installer usage.

### Changed
- **guides/README.md → CACHYOS_QUICK_START.md:** Renamed and clarified as the CachyOS-first entry point.
- **Root README:** Reframed for end-users with quick-start cards for CachyOS, Arch Hybrid, and Fedora guides.
- **Arch & Fedora Guides:** Phases realigned, duplicated content replaced with links to the shared document, and tables of contents refreshed.

### Improved
- **Maintainability:** Single source for distro-agnostic steps.
- **Navigation:** Consistent cross-links between guides, shared doc, and hardware reference.

---

## 2026-03-18 - Second Refactoring Pass

### Changed
- **Phase Numbering:** Fixed sequential phase numbering in Arch Hybrid Guide (Phase 3-5 instead of 4-6)
- **README Structure:** 
  - Reorganized with clearer sections
  - Consolidated key optimizations into single section
  - Improved Table of Contents structure
  - Added Core Philosophy section for better context

### Improved
- **Consistency:** Better alignment between README and detailed guides
- **Navigation:** Clearer section organization and cross-references

---

## 2026-03-18 - Major Refactoring

### Removed
- **NPU (AMD XDNA 2) Content:** Removed all NPU-related sections from all guides
  - Removed Phase 3 from Arch Hybrid Guide
  - Removed NPU content from Fedora Optimized Guide Phase 4
  - Removed NPU section from Hardware Optimization Reference
  - Removed NPU references from README
  - Removed NPU from hardware compatibility tables

- **Arch Phase 4 Simplification:** Removed items 1, 2, and 4
  - Removed CPU Power Scaling (amd_pstate=active) configuration
  - Removed Boot-time power tuning (powertop service)
  - Removed Auto-Brightness (wluma) setup
  - Kept ZRAM, Battery Longevity, and Wi-Fi powersave fix

- **Script References:** Removed all script references except `install_fedora_thai_config.sh`
  - Removed `system_info_report.sh`
  - Removed `flatpak-kde-manager.sh`
  - Removed `steam_cache_relocator.sh`
  - Removed `cleanup_fonts.sh`
  - Removed `howdy_camera.te/.pp` references
  - Kept only `install_fedora_thai_config.sh` as requested

### Changed
- **Hardware Compatibility Tables:** Consolidated into single table in Hardware_Optimization_Reference.md
  - Both Arch and Fedora guides now reference the centralized table
  - Eliminates duplicate maintenance
  - Single source of truth for hardware status

- **README Structure:** Enhanced organization and navigation
  - Added Quick Start section
  - Added Table of Contents
  - Improved section headers and numbering
  - Better guide relationship explanation

- **Markdown Formatting:** Standardized across all guides
  - Consistent list formatting (removed trailing periods)
  - Standardized heading hierarchy
  - Improved code block formatting
  - Cleaner cross-references

### Improved
- **Navigation:** Better cross-referencing between guides
- **Consistency:** Unified tone and formatting across all documents
- **Maintainability:** Reduced duplication makes updates easier

### Files Modified
- `README.md`
- `Arch_Hybrid_Guide.md`
- `Fedora_Optimized_Guide.md`
- `Hardware_Optimization_Reference.md`
- `CHANGELOG.md` (new)

### Technical Accuracy
All command snippets, file paths, and technical details remain accurate. No functionality was altered, only documentation structure and content organization.
