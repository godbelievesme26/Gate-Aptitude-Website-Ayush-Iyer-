import pymupdf
from PIL import Image, ImageChops
from pathlib import Path
import hashlib
import json

ROOT = Path('.')
PDF = 'internal/ae/AE2025.pdf'
doc = pymupdf.open(PDF)

# Directory for figures
(ROOT / 'figures').mkdir(parents=True, exist_ok=True)

# Let's map questions to pages and extract their figures
FIGURE_DEFS = {
    20: (15, "Pair of point vortices with clockwise circulation Γ separated by distance a and centroid O."),
    27: (19, "Simply supported horizontal beam AB of length L with linearly varying distributed transverse load from q0 at A to 0 at B."),
    29: (20, "Uniform symmetric cross-section cantilever beam of length L with transverse force P at free end."),
    30: (21, "Plate ABCD undeformed rhombus (solid lines) with 20 cm diagonals deforming to AC = 19.96 cm and BD = 20.04 cm (dotted lines)."),
    49: (29, "Supersonic stream at Mach 5 turned by a 20 degree ramp, with shock wave and pressure p2/p1 = 7.125."),
    53: (30, "Spacecraft orbit around planet with center O, periapsis P, and points F (OF=8000 km, theta_F=0) and G (OG=10000 km, theta_G=60 deg)."),
    56: (31, "Three-bar truss with joints A, B, C, D and vertical load of 50 N."),
    57: (31, "Uniform rigid bar of mass 3 kg hinged at point F and supported by spring of stiffness k=100 N/m."),
    58: (32, "Prismatic vertical column of cross-section a x 0.5a and length l fixed at bottom, free at top under compressive force P."),
    59: (32, "Thin flat plate stress element subjected to sigma_xx=160 MPa, sigma_yy=40 MPa, tau_xy=80 MPa."),
    60: (33, "Thin-walled closed section designs A and B with semi-circular nose and rectangular extension carrying torque.")
}

OPTION_FIGURE_DEFS = {
    19: (14, {
        'A': 'Pitching moment curve M vs alpha with positive slope and negative zero-lift pitching moment.',
        'B': 'Pitching moment curve M vs alpha with negative slope and positive zero-lift pitching moment.',
        'C': 'Pitching moment curve M vs alpha with negative slope and negative zero-lift pitching moment.',
        'D': 'Pitching moment curve M vs alpha with positive slope and positive zero-lift pitching moment.'
    })
}

print("Testing figure extraction...")

# Let's inspect page 14 option figures
p14 = doc[13]
imgs_14 = p14.get_images()
print(f"Page 14 has {len(imgs_14)} images:")
for idx, im_info in enumerate(imgs_14):
    xref = im_info[0]
    if im_info[2] != 1252 and im_info[2] != 166:
        base_img = doc.extract_image(xref)
        label = ['A', 'B', 'C', 'D'][idx - 2] if idx >= 2 else f"img_{idx}"
        print(f"  xref {xref}: {base_img['width']}x{base_img['height']} -> Option {label}")

# Let's test all single figures
for qnum, (pno, alt) in FIGURE_DEFS.items():
    page = doc[pno - 1]
    imgs = [im for im in page.get_images() if im[2] != 1252 and im[2] != 166]
    print(f"Q.{qnum} (Page {pno}): found {len(imgs)} candidate image(s)")
