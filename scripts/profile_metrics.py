"""Build local SVG metrics using the public GitHub contribution calendar."""

import calendar
import re
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
from urllib.request import Request, urlopen

PALETTE = ['#58e8d4', '#74a7ff', '#b9a1ff', '#f2bb7c', '#f180a5', '#79c8ed', '#99d98c', '#9db6cc']


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.counts = {}
        self.tooltip = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-date' in attrs and 'id' in attrs:
            self.cells[attrs['id']] = date.fromisoformat(attrs['data-date'])
        if tag == 'tool-tip' and attrs.get('for'):
            self.tooltip = attrs['for']
            self.text = []

    def handle_data(self, data):
        if self.tooltip:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.tooltip:
            match = re.match(r'\s*(No|[\d,]+) contributions?\b', ''.join(self.text))
            if match:
                self.counts[self.tooltip] = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
            self.tooltip = None


def fetch_calendar(username, joined, today):
    days = {}
    for year in range(joined.year, today.year + 1):
        url = f'https://github.com/users/{username}/contributions?from={year}-01-01&to={year}-12-31'
        request = Request(url, headers={'User-Agent': 'GDJ2001-profile', 'Accept-Language': 'en-US'})
        with urlopen(request, timeout=30) as response:
            parser = CalendarParser()
            parser.feed(response.read().decode('utf-8'))
        for element_id, day in parser.cells.items():
            if joined <= day <= today and day.year == year:
                if element_id not in parser.counts:
                    raise ValueError(f'Missing contribution count for {day}; keeping previous cards.')
                days[day] = parser.counts[element_id]
    expected = {joined + timedelta(days=n) for n in range((today - joined).days + 1)}
    if set(days) != expected:
        raise ValueError('Incomplete public contribution calendar; keeping previous cards.')
    return days


def streaks(days, today):
    longest = 0
    longest_start = longest_end = None
    run = 0
    start = previous = None
    for day, count in sorted(days.items()):
        if count:
            if previous is None or day != previous + timedelta(days=1) or run == 0:
                run, start = 0, day
            run += 1
            if run > longest:
                longest, longest_start, longest_end = run, start, day
        else:
            run = 0
        previous = day
    end = today if days.get(today, 0) else today - timedelta(days=1)
    cursor, current = end, 0
    while days.get(cursor, 0):
        current += 1
        cursor -= timedelta(days=1)
    return {'current': current, 'current_start': cursor + timedelta(days=1) if current else None,
            'current_end': end if current else None, 'longest': longest,
            'longest_start': longest_start, 'longest_end': longest_end}


def text(x, y, value, size=16, color='#b5c6d8', anchor='start', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(value))}</text>'


def card(width, height, title, content, today):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}. Updated {today.isoformat()} UTC.</title>
<rect width="{width}" height="{height}" rx="16" fill="#0b1627"/>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="16" fill="none" stroke="#263a54"/>
<g font-family="Segoe UI,Arial,sans-serif">{content}
{text(width / 2, height - 20, 'UPDATED ' + today.strftime('%d %b %Y').upper() + ' UTC', 11, '#8da9c0', 'middle')}
</g></svg>\n'''


def date_range(start, end):
    if not start:
        return 'No active streak'
    return f'{start:%d %b %Y} – {end:%d %b %Y}'


def streak_card(days, today, mobile=False):
    s = streaks(days, today)
    metrics = [('TOTAL CONTRIBUTIONS', f'{sum(days.values()):,}', date_range(min(days), today)),
               ('CURRENT STREAK', f"{s['current']} days", date_range(s['current_start'], s['current_end'])),
               ('LONGEST STREAK', f"{s['longest']} days", date_range(s['longest_start'], s['longest_end']))]
    width, height = (480, 470) if mobile else (960, 270)
    content = text(28, 37, 'CONTRIBUTIONS & CONSISTENCY', 14, '#e6edf3', weight=600)
    for index, (label, value, period) in enumerate(metrics):
        x, y = (240, 103 + index * 120) if mobile else (160 + index * 320, 128)
        content += text(x, y, value, 38, PALETTE[index], 'middle', 700)
        content += text(x, y + 30, label, 12, '#d5e2ef', 'middle', 600)
        content += text(x, y + 54, period, 12, '#8da9c0', 'middle')
    if not mobile:
        content += '<path d="M320 72V195M640 72V195" stroke="#263a54"/>'
    content += text(width / 2, height - 44, 'All-time public profile activity · Daily streaks', 12, '#8da9c0', 'middle')
    title = '; '.join(f'{label}: {value}, {period}' for label, value, period in metrics)
    return card(width, height, title, content, today)


def language_card(languages, repo_count, today, mobile=False):
    ranked = sorted(languages.items(), key=lambda item: (-item[1], item[0]))
    total = sum(languages.values())
    shown = ranked[:7]
    if len(ranked) > 7:
        shown.append(('Other', sum(value for _, value in ranked[7:])))
    width = 480 if mobile else 960
    height = 150 + len(shown) * 59
    content = text(28, 38, 'MOST USED LANGUAGES', 19, '#e6edf3', weight=600)
    content += text(28, 65, f'Code volume across {repo_count} public non-fork repositories', 12)
    if not total:
        content += text(28, 110, 'No language data available yet.', 16)
    for index, (language, value) in enumerate(shown):
        y = 102 + index * 59
        percent = 100 * value / total
        content += text(28, y, language, 15, '#d5e2ef', weight=600)
        content += text(width - 28, y, f'{percent:.1f}%', 14, PALETTE[index], 'end')
        content += f'<rect x="28" y="{y + 12}" width="{width - 56}" height="10" rx="5" fill="#1b2b40"/>'
        content += f'<rect x="28" y="{y + 12}" width="{(width - 56) * percent / 100:.2f}" height="10" rx="5" fill="{PALETTE[index]}"/>'
    content += text(28, height - 46, 'Based on repository bytes; not a measure of proficiency.', 12, '#8da9c0')
    return card(width, height, 'Most used languages by public repository code volume', content, today)


def monthly_card(days, today, mobile=False):
    # Twelve calendar months, including the current partial month.
    months = []
    for offset in range(11, -1, -1):
        absolute = today.year * 12 + today.month - 1 - offset
        months.append((absolute // 12, absolute % 12 + 1))
    totals = [sum(count for day, count in days.items() if (day.year, day.month) == key) for key in months]
    start = date(*months[0], 1)
    active = sum(count > 0 for day, count in days.items() if day >= start)
    width, height = (480, 480) if mobile else (960, 350)
    content = text(28, 38, 'MONTHLY CONTRIBUTION ACTIVITY', 16, '#e6edf3', weight=600)
    content += text(28, 66, f'{sum(totals):,} contributions · {active} active days', 16, '#58e8d4', weight=600)
    maximum = max(totals, default=0) or 1
    if mobile:
        for index, ((year, month), count) in enumerate(zip(months, totals)):
            y = 100 + index * 26
            content += text(28, y + 12, f'{calendar.month_abbr[month]} {year % 100:02}', 12)
            content += f'<rect x="95" y="{y}" width="{max(2, 290 * count / maximum):.2f}" height="15" rx="3" fill="{PALETTE[0] if index == 11 else PALETTE[1]}"/>'
            content += text(452, y + 12, f'{count:,}', 12, '#d5e2ef', 'end')
    else:
        for index, ((year, month), count) in enumerate(zip(months, totals)):
            x = 60 + index * 76
            bar_height = max(2, 135 * count / maximum)
            content += f'<rect x="{x - 21}" y="{252 - bar_height:.2f}" width="42" height="{bar_height:.2f}" rx="5" fill="{PALETTE[0] if index == 11 else PALETTE[1]}"/>'
            content += text(x, 241 - bar_height, f'{count:,}', 12, '#d5e2ef', 'middle')
            content += text(x, 277, calendar.month_abbr[month], 12, '#b5c6d8', 'middle')
            content += text(x, 294, str(year), 10, '#8da9c0', 'middle')
    content += text(width / 2, height - 43, 'Last 12 calendar months · Current month is partial', 12, '#8da9c0', 'middle')
    return card(width, height, 'Monthly contribution activity over twelve calendar months', content, today)


def calculate_grade(data, public_stars):
    """Implement the public GitHub Readme Stats rank formula."""
    values = {
        'commits': data['commits']['totalCommitContributions'],
        'pull requests': data['pullRequests']['totalCount'],
        'issues': data['openedIssues']['totalCount'] + data['closedIssues']['totalCount'],
        'reviews': data['reviews']['totalPullRequestReviewContributions'],
        'stars': public_stars,
        'followers': data['followers']['totalCount'],
    }
    weights = {'commits': 2, 'pull requests': 3, 'issues': 1,
               'reviews': 1, 'stars': 4, 'followers': 1}
    medians = {'commits': 250, 'pull requests': 50, 'issues': 25,
               'reviews': 2, 'stars': 50, 'followers': 10}
    rank_sum = 0.0
    for metric, value in values.items():
        ratio = value / medians[metric]
        cdf = ratio / (1 + ratio) if metric in ('stars', 'followers') else 1 - 2 ** -ratio
        rank_sum += weights[metric] * cdf
    score = 100 * rank_sum / sum(weights.values())
    boundaries = [(99, 'S'), (87.5, 'A+'), (75, 'A'), (62.5, 'A-'),
                  (50, 'B+'), (37.5, 'B'), (25, 'B-'), (12.5, 'C+'), (0, 'C')]
    grade = next((letter for minimum, letter in boundaries if score >= minimum), 'C')
    return {'grade': grade, 'score': max(0, min(100, score)), 'inputs': values,
            'commits_year': datetime.now(timezone.utc).year}


def grade_card(grade, today, mobile=False):
    width, height = (480, 430) if mobile else (960, 300)
    score = grade['score']
    grade_color = '#58e8d4' if grade['grade'] in ('S', 'A+', 'A') else '#74a7ff' if grade['grade'] in ('A-', 'B+', 'B') else '#f2bb7c'
    content = text(28, 38, 'COMMUNITY PROFILE RANK', 16, '#e6edf3', weight=600)
    if mobile:
        content += f'<circle cx="240" cy="143" r="64" fill="#102339" stroke="#263a54" stroke-width="10"/>'
        content += f'<circle cx="240" cy="143" r="64" fill="none" stroke="{grade_color}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{2 * 3.14159 * 64 * score / 100:.2f} {2 * 3.14159 * 64:.2f}" transform="rotate(-90 240 143)"/>'
        content += text(240, 159, grade['grade'], 40, grade_color, 'middle', 700)
        content += text(240, 238, f"{score:.1f} / 100 weighted rank score", 18, '#d5e2ef', 'middle', 600)
        content += text(240, 270, 'GitHub Readme Stats rank model', 13, '#8da9c0', 'middle')
        for i, metric in enumerate(('commits', 'pull requests', 'issues', 'reviews', 'stars', 'followers')):
            col, row = i % 2, i // 2
            value = grade['inputs'][metric]
            label = 'commits ' + str(grade['commits_year']) if metric == 'commits' else metric
            content += text(35 + col * 230, 316 + row * 28, f'{label}: {value:,}', 13, '#b5c6d8')
    else:
        content += '<path d="M250 78V222M700 78V222" stroke="#263a54"/>'
        content += f'<circle cx="145" cy="149" r="65" fill="#102339" stroke="#263a54" stroke-width="10"/>'
        content += f'<circle cx="145" cy="149" r="65" fill="none" stroke="{grade_color}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{2 * 3.14159 * 65 * score / 100:.2f} {2 * 3.14159 * 65:.2f}" transform="rotate(-90 145 149)"/>'
        content += text(145, 165, grade['grade'], 40, grade_color, 'middle', 700)
        content += text(335, 124, f"{score:.1f} / 100", 32, grade_color, weight=700)
        content += text(335, 154, 'weighted rank score', 15, '#d5e2ef', weight=600)
        content += text(335, 184, 'GitHub Readme Stats rank model', 13, '#8da9c0')
        metrics = list(grade['inputs'].items())
        for index, (label, value) in enumerate(metrics):
            col, row = index % 2, index // 2
            x, y = 748 + col * 112, 105 + row * 36
            label = f"{grade['commits_year']} commits" if label == 'commits' else label
            content += text(x, y, f'{value:,}', 17, PALETTE[index], weight=700)
            content += text(x, y + 16, label, 10, '#b5c6d8')
    content += text(width / 2, height - 46, 'A GitHub activity rank · Not a measure of engineering skill', 12, '#8da9c0', 'middle')
    return card(width, height, f"GitHub Readme Stats community rank {grade['grade']}, weighted score {score:.1f} out of 100", content, today)


def build_metrics(user, repos, github, rank_data):
    today = datetime.now(timezone.utc).date()
    joined = date.fromisoformat(user['created_at'][:10])
    days = fetch_calendar(user['login'], joined, today)
    languages = Counter()
    eligible = [repo for repo in repos if not repo['fork'] and repo['name'] != user['login']]
    for repo in eligible:
        languages.update(github(f"repos/{repo['full_name']}/languages"))
    artifacts = {}
    for mobile in (False, True):
        suffix = '-mobile' if mobile else ''
        artifacts[f'contribution-streaks{suffix}.svg'] = streak_card(days, today, mobile)
        artifacts[f'top-languages{suffix}.svg'] = language_card(languages, len(eligible), today, mobile)
        artifacts[f'contribution-activity{suffix}.svg'] = monthly_card(days, today, mobile)
    public_stars = sum(repo['stargazers_count'] for repo in repos)
    grade = calculate_grade(rank_data, public_stars)
    for mobile in (False, True):
        suffix = '-mobile' if mobile else ''
        artifacts[f'github-grade{suffix}.svg'] = grade_card(grade, today, mobile)
    summary = streaks(days, today)
    print(f"Contributions: {sum(days.values()):,}; current streak: {summary['current']}; longest: {summary['longest']}; languages: {len(languages)}; profile rank {grade['grade']} ({grade['score']:.1f}).")
    return artifacts
