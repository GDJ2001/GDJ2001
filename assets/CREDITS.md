# Visual credits & maintenance

The header, engineering diagram, footer, and statistics card are custom SVG artwork created for this profile. Animations use CSS inside SVG images, include reduced-motion support, and keep all text visible when animation is unavailable.

Technology icon strips are assembled from the original SVGs in [Skill Icons](https://github.com/tandpfun/skill-icons/tree/main/icons) and stored locally so visiting the profile does not require the icon service. Its MIT license is included in [skill-icons-LICENSE.txt](skill-icons-LICENSE.txt). Technology logos belong to their respective owners.

The GitHub card uses public repository and follower data from the [GitHub REST API](https://docs.github.com/en/rest). It shows a dated snapshot, refreshed daily by [profile-stats.yml](../.github/workflows/profile-stats.yml). The workflow uses the repository's built-in token; no personal access token or external image host is required. Failed refreshes retain the last successful card.

To refresh manually, run `python scripts/update_profile.py` from the repository root, or run **Refresh profile statistics** in GitHub Actions. Stars are the sum across all public repositories returned for the profile, including any public forks. Private repositories and their metadata are excluded.

Layout references: [GitHub Markdown formatting](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github) and [README Typing SVG](https://github.com/DenverCoder1/readme-typing-svg). The custom header does not depend on a hosted typing service.

## Contribution and language components

The streak component follows the familiar total/current/longest structure of [GitHub README Streak Stats](https://github.com/DenverCoder1/github-readme-streak-stats). The SVG artwork and implementation here are custom and generated locally by the existing workflow.

- **Total contributions:** sum of daily counts from the public GitHub contribution calendar, from account creation through the refresh date. Includes all contribution types GitHub counts, not just commits. Anonymous private contribution counts may be included if enabled on the public profile; no private repository names or contents are requested.
- **Current streak:** consecutive contribution days ending today, or yesterday when today has no contributions yet. A missed completed day resets the streak. The refresh uses UTC and GitHub's calendar date labels.
- **Longest streak:** the longest consecutive run across the entire available history, including runs crossing a year boundary. For equal runs, the earliest is shown.
- **Monthly activity:** twelve calendar months ending with the current partial month. Active days have at least one contribution. The total here covers this displayed period, unlike the all-time total above.
- **Languages:** summed bytes from the [GitHub repository languages endpoint](https://docs.github.com/en/rest/repos/repos#list-repository-languages), across public owned repositories excluding forks and this generated profile repository. Shows the seven largest language categories plus Other when needed. Includes archived repositories. These percentages describe repository contents, not personal proficiency or authorship.

The calendar is fetched without authentication, so the statistics match what public visitors can see. Each year must have complete daily counts; an unexpected HTML format, missing day, or network/API error fails the refresh and preserves the existing cards. All cards are snapshots, so a new contribution appears after a successful refresh. The workflow can also be run manually from the Actions tab.
