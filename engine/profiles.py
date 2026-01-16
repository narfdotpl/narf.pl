from __future__ import annotations
from dataclasses import dataclass
from markupsafe import Markup


@dataclass
class Profile:
    name: str
    id: str
    url: str
    tag: str
    handle: str
    icon_class: str
    hidden: bool

    @classmethod
    def make(cls, name: str, url: str, handle: str = '@narfdotpl', hidden: bool = False) -> Profile:
        id = name.replace('.', '').lower()
        tag = Markup(f'<a href="{url}" rel="me">{name}</a>')
        return Profile(
            name=name,
            id=id,
            url=url,
            tag=tag,
            handle=handle,
            icon_class=f'fab fa-lg fa-{id}',
            hidden=hidden,
        )


ps = [
    Profile.make('Mastodon', 'https://vis.social/@narf', '@narf@vis.social'),
    Profile.make('Bandcamp', 'https://narfdotpl.bandcamp.com/'),
    Profile.make('Instagram', 'https://www.instagram.com/narfdotpl/'),
    Profile.make('YouTube', 'https://www.youtube.com/@narfdotpl'),
    Profile.make('GitHub', 'https://github.com/narfdotpl'),

    Profile.make('Spotify', 'https://open.spotify.com/artist/54VsVeo4UsHNvTXN5wz9kR', hidden=True),
    Profile.make('Last.fm', 'http://www.last.fm/user/narfdotpl', hidden=True),
    Profile.make('LinkedIn', 'https://www.linkedin.com/in/narfdotpl/', hidden=True),
]

profiles = {p.id: p for p in ps}
profiles['all'] = ps
profiles['visible'] = [p for p in ps if not p.hidden]
