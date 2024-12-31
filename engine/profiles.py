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


profiles = {p.id: p for p in [
    Profile.make('Mastodon', 'https://vis.social/@narf', '@narf@vis.social'),
    Profile.make('Instagram', 'https://www.instagram.com/narfdotpl/'),
    Profile.make('Threads', 'https://www.threads.net/@narfdotpl'),
    Profile.make('LinkedIn', 'https://www.linkedin.com/in/narfdotpl/', hidden=True),
    Profile.make('Bandcamp', 'https://narfdotpl.bandcamp.com/'),
    Profile.make('Spotify', 'https://open.spotify.com/artist/54VsVeo4UsHNvTXN5wz9kR'),
    Profile.make('Last.fm', 'http://www.last.fm/user/narfdotpl'),
    Profile.make('GitHub', 'https://github.com/narfdotpl'),
]}
