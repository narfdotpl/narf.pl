from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Profile:
    name: str
    id: str
    url: str
    handle: str
    icon_class: str

    @classmethod
    def make(cls, name: str, url: str, handle: str = '@narfdotpl') -> Profile:
        id = name.replace('.', '').lower()
        return Profile(
            name=name,
            id=id,
            url=url,
            handle=handle,
            icon_class=f'fab fa-lg fa-{id}',
        )


profiles = {p.id: p for p in [
    Profile.make('Mastodon', 'https://vis.social/@narf', '@narf@vis.social'),
    Profile.make('Instagram', 'https://www.instagram.com/narfdotpl/'),
    Profile.make('Bandcamp', 'https://narfdotpl.bandcamp.com/'),
    Profile.make('Spotify', 'https://open.spotify.com/artist/54VsVeo4UsHNvTXN5wz9kR'),
    Profile.make('Last.fm', 'http://www.last.fm/user/narfdotpl'),
    Profile.make('GitHub', 'https://github.com/narfdotpl'),
]}
