# Visual credits & maintenance

The header, engineering diagram, footer, and statistics card are custom SVG artwork created for this profile. Animations use CSS inside SVG images, include reduced-motion support, and keep all text visible when animation is unavailable.

Technology icon strips are assembled from the original SVGs in [Skill Icons](https://github.com/tandpfun/skill-icons/tree/main/icons) and stored locally so visiting the profile does not require the icon service. Its MIT license is included in [skill-icons-LICENSE.txt](skill-icons-LICENSE.txt). Technology logos belong to their respective owners.

The GitHub card uses public repository and follower data from the [GitHub REST API](https://docs.github.com/en/rest). It shows a dated snapshot, refreshed daily by [profile-stats.yml](../.github/workflows/profile-stats.yml). The workflow uses the repository's built-in token; no personal access token or external image host is required. Failed refreshes retain the last successful card.

To refresh manually, run `python scripts/update_profile.py` from the repository root, or run **Refresh profile statistics** in GitHub Actions. Stars are the sum across all public repositories returned for the profile, including any public forks. Private repositories and their metadata are excluded.

Layout references: [GitHub Markdown formatting](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github) and [README Typing SVG](https://github.com/DenverCoder1/readme-typing-svg). The custom header does not depend on a hosted typing service.
