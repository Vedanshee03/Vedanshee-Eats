/* Theatre shows seen in NYC, one pin per venue */

const THEATRES = {
  "new-amsterdam": { name: "New Amsterdam Theatre", neighborhood: "Times Square", address: "214 W 42nd St, New York, NY 10036", lat: 40.756000, lng: -73.988063 },
  "eugene-oneill": { name: "Eugene O'Neill Theatre", neighborhood: "Theater District", address: "230 W 49th St, New York, NY 10019", lat: 40.761105, lng: -73.985740 },
  "gershwin":      { name: "Gershwin Theatre", neighborhood: "Theater District", address: "222 W 51st St, New York, NY 10019", lat: 40.762362, lng: -73.985204 },
  "koch":          { name: "David H. Koch Theater", neighborhood: "Lincoln Center", address: "20 Lincoln Center Plaza, New York, NY 10023", lat: 40.771795, lng: -73.983766 },
  "ambassador":    { name: "Ambassador Theatre", neighborhood: "Theater District", address: "219 W 49th St, New York, NY 10019", lat: 40.761236, lng: -73.984990 },
  "hirschfeld":    { name: "Al Hirschfeld Theatre", neighborhood: "Theater District", address: "302 W 45th St, New York, NY 10036", lat: 40.759253, lng: -73.989211 },
  "marquis":       { name: "Marquis Theatre", neighborhood: "Times Square", address: "210 W 46th St, New York, NY 10036", lat: 40.758904, lng: -73.986185 },
  "winter-garden": { name: "Winter Garden Theatre", neighborhood: "Theater District", address: "1634 Broadway, New York, NY 10019", lat: 40.761686, lng: -73.983505 },
  "radio-city":    { name: "Radio City Music Hall", neighborhood: "Rockefeller Center", address: "1260 6th Ave, New York, NY 10020", lat: 40.759812, lng: -73.979279 },
  "sondheim":      { name: "Stephen Sondheim Theatre", neighborhood: "Times Square", address: "124 W 43rd St, New York, NY 10036", lat: 40.755896, lng: -73.984933 },
};

const SHOWS = [
  { title: "Aladdin", kind: "Musical", theatre: "new-amsterdam" },
  { title: "The Book of Mormon", kind: "Musical", theatre: "eugene-oneill" },
  { title: "Wicked", kind: "Musical", theatre: "gershwin" },
  { title: "The Nutcracker", kind: "Ballet", theatre: "koch" },
  { title: "Chicago", kind: "Musical", theatre: "ambassador" },
  { title: "Moulin Rouge!", kind: "Musical", theatre: "hirschfeld" },
  { title: "Stranger Things: The First Shadow", kind: "Play", theatre: "marquis" },
  { title: "The Sleeping Beauty", kind: "Ballet", theatre: "koch" },
  { title: "Much Ado About Nothing", kind: "Play", theatre: "winter-garden" },
  { title: "Christmas Spectacular starring the Radio City Rockettes", kind: "Spectacular", theatre: "radio-city" },
  { title: "& Juliet", kind: "Musical", theatre: "sondheim" },
];
