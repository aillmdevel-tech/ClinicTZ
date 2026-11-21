import bpy, math, sys
from mathutils import Euler

OUT = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

MATS = {}
def mat(name, rgb, rough=0.9, emit=0.0):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1)
        b.inputs["Emission Strength"].default_value = emit
    MATS[name] = m; return m

def box(loc, size, m, rot=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = size; o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def limb(loc, size, m, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.5, depth=1, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = size; o.data.materials.append(m); bpy.ops.object.shade_flat(); return o

def cyl(loc, r, d, m, v=8, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot)
    o = bpy.context.object; o.data.materials.append(m); return o

def head(loc, m):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=7, radius=0.12, location=loc)
    o = bpy.context.object; o.scale = (0.95, 1.0, 1.12); o.data.materials.append(m)
    bpy.ops.object.shade_flat(); return o

def text(s, loc, size=0.13, m=None):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0))
    t = bpy.context.object; t.data.body = s; t.data.size = size; t.data.align_x = "CENTER"
    try: t.data.font = bpy.data.fonts.load("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
    except Exception: pass
    t.data.materials.append(m or mat("label", (0.95, 0.92, 0.8), emit=1.5)); return t

SKIN = [(0.80, 0.60, 0.47), (0.62, 0.43, 0.31), (0.86, 0.68, 0.56), (0.70, 0.50, 0.38)]
WHITE = mat("coat", (0.7, 0.71, 0.67))
GLOVE = mat("glove", (0.55, 0.75, 0.86), rough=0.4)
SHOE = mat("shoe", (0.08, 0.08, 0.08))
BLACK = mat("black", (0.01, 0.01, 0.01))
RED = mat("red", (0.55, 0.05, 0.04))

def figure(x, kind, scrub=(0.2, 0.6, 0.6), skin=SKIN[0], nick="", label=""):
    # kind: doctor | patient | double_patient | double_doctor
    sk = mat(f"skin{skin}", skin)
    doctor = kind in ("doctor", "double_doctor")
    pants = mat(f"scrub{scrub}", scrub) if doctor else mat("track", (0.07, 0.1, 0.32))
    top = pants
    # legs + shoes
    for s in (-1, 1):
        limb((x + s * 0.095, 0, 0.45), (0.15, 0.17, 0.82), pants)
        box((x + s * 0.1, -0.04, 0.04), (0.16, 0.26, 0.08), SHOE if doctor else mat("sneaker", (0.85, 0.85, 0.85)))
    # torso
    t=limb((x, 0, 1.14), (0.40, 0.25, 0.62), top)
    if doctor:  # open white coat: back + two front panels + long tail
        limb((x, 0.02, 1.02), (0.47, 0.27, 0.96), WHITE)
        for s in (-1, 1):
            box((x + s * 0.15, -0.12, 1.02), (0.13, 0.04, 0.96), WHITE)
        # badge
        bm = mat(f"badge{nick}", (0.95, 0.95, 0.9)) if kind == "doctor" else BLACK
        box((x - 0.17, -0.15, 1.28), (0.12, 0.01, 0.08), bm)
        box((x - 0.17, -0.155, 1.31), (0.12, 0.01, 0.02), mat(f"scrub{scrub}", scrub))
        # flashlight in pocket
        cyl((x + 0.17, -0.15, 1.1), 0.025, 0.14, BLACK)
    else:  # tracksuit stripes
        for s in (-1, 1):
            box((x + s * 0.2, -0.125, 1.12), (0.03, 0.01, 0.6), mat("stripe", (0.9, 0.9, 0.9)))
    # arms
    long = 1.25 if kind == "double_doctor" else 1.0
    for s in (-1, 1):
        L = 0.62 * (long if s == 1 else 1.0)
        limb((x + s * 0.27, 0, 1.4 - L / 2), (0.11, 0.12, L), WHITE if doctor else pants, rot=(0, math.radians(-s*4), 0))
        box((x + s * 0.29, 0, 1.4 - L - 0.05), (0.08, 0.1, 0.13), GLOVE if doctor else sk)
    # neck + head
    limb((x, 0, 1.48), (0.1, 0.1, 0.1), sk)
    tilt = {"double_doctor": 28, "double_patient": -18}.get(kind, 0)
    h = head((x, 0, 1.64), sk); h.rotation_euler = Euler((0, math.radians(tilt), 0))
    def face(dx, dz, size, m):
        o = box((x + dx, -0.125, 1.64 + dz), size, m); o.parent = h
        o.matrix_parent_inverse = h.matrix_world.inverted(); return o
    if kind == "double_doctor":
        pass  # smooth face: no eyes, no mouth
    elif kind == "double_patient":
        face(-0.05, 0.03, (0.06, 0.02, 0.05), BLACK); face(0.05, 0.03, (0.06, 0.02, 0.05), BLACK)
        face(0, -0.06, (0.19, 0.02, 0.035), RED)  # ear-to-ear grin
    else:
        face(-0.045, 0.03, (0.035, 0.02, 0.025), BLACK); face(0.045, 0.03, (0.035, 0.02, 0.025), BLACK)
        face(0, -0.055, (0.06, 0.02, 0.012), mat("lip", (0.35, 0.15, 0.12)))
    if doctor:
        c = cyl((x, 0, 1.79), 0.14, 0.09, mat(f"scrub{scrub}", scrub), v=10)
        c.parent = h; c.matrix_parent_inverse = h.matrix_world.inverted()
        box((x, -0.08, 1.46), (0.16, 0.04, 0.05), GLOVE)  # mask on neck
    else:
        hair = box((x, 0.02, 1.77), (0.27, 0.27, 0.08), mat("hair", (0.12, 0.08, 0.05)))
        hair.parent = h; hair.matrix_parent_inverse = h.matrix_world.inverted()
    if nick: text(nick, (x, -0.3, 1.98), 0.08)
    if False: text(label, (x, -0.4, -0.18), 0.085, mat("label2", (0.75, 0.75, 0.7), emit=1.0))

# room: green lower wall, beige upper, tiled floor
box((0, 1.2, 0.6), (12, 0.05, 1.2), mat("wall_lo", (0.22, 0.32, 0.25)))
box((0, 1.2, 2.1), (12, 0.05, 1.8), mat("wall_hi", (0.62, 0.58, 0.46)))
floor = box((0, -1, -0.01), (12, 6, 0.02), mat("floor", (0.4, 0.42, 0.38)))
fm = floor.data.materials[0]; nt = fm.node_tree
ch = nt.nodes.new("ShaderNodeTexChecker"); ch.inputs["Scale"].default_value = 40
ch.inputs["Color1"].default_value = (0.42, 0.44, 0.4, 1); ch.inputs["Color2"].default_value = (0.25, 0.28, 0.25, 1)
nt.links.new(ch.outputs["Color"], next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED").inputs["Base Color"])
box((-3.6, 1.14, 1.75), (0.5, 0.02, 0.7), mat("poster", (0.8, 0.75, 0.6)))
box((-3.6, 1.12, 1.85), (0.18, 0.02, 0.18), RED)

xs = [-3.15, -2.1, -1.05, 0.0, 1.05, 2.1, 3.15]
figure(xs[0], "doctor", (0.18, 0.45, 0.45), SKIN[0], "ALEX", "doctor 1")
figure(xs[1], "doctor", (0.58, 0.46, 0.14), SKIN[1], "DIMA", "doctor 2")
figure(xs[2], "doctor", (0.6, 0.32, 0.42), SKIN[2], "KATYA", "doctor 3")
figure(xs[3], "doctor", (0.18, 0.26, 0.5), SKIN[3], "MAX", "doctor 4")
figure(xs[4], "patient", skin=SKIN[2], label="patient")
figure(xs[5], "double_patient", skin=SKIN[2], label="double (patient)")
figure(xs[6], "double_doctor", (0.18, 0.45, 0.45), SKIN[0], "ALEX?", "double (colleague)")

# lights: warm fluorescent strips + cold fill
for lx in (-2.5, 0, 2.5):
    bpy.ops.object.light_add(type="AREA", location=(lx, -0.6, 3.0))
    l = bpy.context.object; l.data.shape = "RECTANGLE"; l.data.size = 1.6; l.data.size_y = 0.25
    l.data.energy = 90; l.data.color = (1.0, 0.93, 0.78)
bpy.ops.object.light_add(type="POINT", location=(0, -4, 1.5)); bpy.context.object.data.energy = 25
bpy.context.object.data.color = (0.6, 0.8, 0.85)

w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.005, 0.006, 0.006, 1)

bpy.ops.object.camera_add(location=(0, -9.3, 1.25), rotation=(math.radians(88.5), 0, 0))
cam = bpy.context.object; cam.data.lens = 40; sc.camera = cam

for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
    try: sc.render.engine = eng; break
    except TypeError: pass
try:
    sc.eevee.use_gtao = True; sc.eevee.gtao_distance = 0.6
except Exception: pass
sc.render.resolution_x, sc.render.resolution_y = 960, 400
sc.view_settings.view_transform = "AgX"; sc.view_settings.exposure = -0.3
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace(".png", ".blend"))
