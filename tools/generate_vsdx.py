"""
Generate architecture.vsdx — a project architecture diagram based on the
entire project structure of the Django + Vue3 research management system.
"""
import zipfile
import xml.etree.ElementTree as ET
import os
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_VSDX = os.path.join(BASE_DIR, 'zwm.vsdx')
OUT_VSDX = os.path.join(BASE_DIR, 'architecture.vsdx')

NS = 'http://schemas.microsoft.com/office/visio/2012/main'

# Register default namespace to avoid ns0: prefix in serialized XML
ET.register_namespace('', NS)
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')


def serialize_xml(elem, root_tag_is_page_contents=True):
    """Serialize element tree to proper Visio-compatible XML string."""
    raw = ET.tostring(elem, encoding='unicode')
    # Add XML declaration
    result = '<?xml version="1.0" encoding="utf-8" ?>\n' + raw
    # Fix xml:space attribute — ET sometimes mangles it
    result = result.replace('xml_space', 'xml:space')
    return result


def add_shape_props(shape, pin_x, pin_y, width, height):
    """Add standard shape positioning cells."""
    ET.SubElement(shape, f'{{{NS}}}Cell', N='PinX', V=str(pin_x))
    ET.SubElement(shape, f'{{{NS}}}Cell', N='PinY', V=str(pin_y))
    ET.SubElement(shape, f'{{{NS}}}Cell', N='Width', V=str(width))
    ET.SubElement(shape, f'{{{NS}}}Cell', N='Height', V=str(height))
    ET.SubElement(shape, f'{{{NS}}}Cell', N='LocPinX', V=str(width/2), F='Width*0.5')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='LocPinY', V=str(height/2), F='Height*0.5')

    # Character section
    char_sec = ET.SubElement(shape, f'{{{NS}}}Section', N='Character')
    char_row = ET.SubElement(char_sec, f'{{{NS}}}Row', IX='0')
    ET.SubElement(char_row, f'{{{NS}}}Cell', N='Size', V='0.1666666666666667', U='PT')
    ET.SubElement(char_row, f'{{{NS}}}Cell', N='Color', V='#000000')

    # Text block
    ET.SubElement(shape, f'{{{NS}}}Cell', N='TxtWidth', V=str(width * 0.9), F='Width*0.9')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='TxtPinX', V=str(width/2), F='Width*0.5')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='TxtPinY', V=str(height/2), F='Height*0.5')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='TxtLocPinX', V=str(width*0.45), F='TxtWidth*0.5')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='TxtLocPinY', V=str(height*0.45), F='TxtHeight*0.5')


def add_text(shape, text_content):
    """Add text element to shape."""
    text_el = ET.SubElement(shape, f'{{{NS}}}Text')
    text_el.text = text_content


def make_connector(shape_id, beg_x, beg_y, end_x, end_y):
    """Create a connector arrow between two points."""
    shape = ET.Element(f'{{{NS}}}Shape', ID=str(shape_id), Type='Shape', Master='6')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='PinX', V=str((beg_x + end_x) / 2), F='Inh')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='PinY', V=str((beg_y + end_y) / 2), F='Inh')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='BeginX', V=str(beg_x))
    ET.SubElement(shape, f'{{{NS}}}Cell', N='BeginY', V=str(beg_y))
    ET.SubElement(shape, f'{{{NS}}}Cell', N='EndX', V=str(end_x))
    ET.SubElement(shape, f'{{{NS}}}Cell', N='EndY', V=str(end_y))
    ET.SubElement(shape, f'{{{NS}}}Cell', N='LineColor', V='#888888')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='LinePattern', V='1')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='LineWeight', V='0.005')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='EndArrow', V='5')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='EndArrowSize', V='2')

    # Geometry section
    geo = ET.SubElement(shape, f'{{{NS}}}Section', N='Geometry', IX='0')
    r1 = ET.SubElement(geo, f'{{{NS}}}Row', T='MoveTo', IX='1')
    ET.SubElement(r1, f'{{{NS}}}Cell', N='X', V=str(beg_x))
    ET.SubElement(r1, f'{{{NS}}}Cell', N='Y', V=str(beg_y))
    r2 = ET.SubElement(geo, f'{{{NS}}}Row', T='LineTo', IX='2')
    ET.SubElement(r2, f'{{{NS}}}Cell', N='X', V=str(end_x))
    ET.SubElement(r2, f'{{{NS}}}Cell', N='Y', V=str(end_y))

    # Character section
    char_s = ET.SubElement(shape, f'{{{NS}}}Section', N='Character')
    char_r = ET.SubElement(char_s, f'{{{NS}}}Row', IX='0')
    ET.SubElement(char_r, f'{{{NS}}}Cell', N='Size', V='0.08333333333333333', U='PT')

    return shape


def make_label_shape(sid, x, y, w, h, text, fill_color):
    """Create a labeled rectangle shape."""
    shape = ET.Element(f'{{{NS}}}Shape',
        ID=str(sid), NameU='Rectangle', Name=text.split('\n')[0],
        Type='Shape', Master='2')
    add_shape_props(shape, x, y, w, h)
    ET.SubElement(shape, f'{{{NS}}}Cell', N='FillForegnd', V=fill_color)
    ET.SubElement(shape, f'{{{NS}}}Cell', N='FillPattern', V='1')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='LinePattern', V='0')
    ET.SubElement(shape, f'{{{NS}}}Cell', N='Rounding', V='0.03')
    # Override text color to white for dark backgrounds
    char_s = shape.find(f'{{{NS}}}Section[@N="Character"]')
    char_r = char_s.find(f'{{{NS}}}Row')
    ET.SubElement(char_r, f'{{{NS}}}Cell', N='Color', V='#ffffff')
    # Adjust font size based on shape size
    ET.SubElement(char_r, f'{{{NS}}}Cell', N='Size', V='0.1111111111111111', U='PT')
    add_text(shape, text)
    return shape


def generate():
    print("Reading template VSDX...")
    with zipfile.ZipFile(SRC_VSDX, 'r') as zin:
        template_files = {name: zin.read(name) for name in zin.namelist()}

    # ─── Build the architecture diagram ───────────────────────────────────────
    page = ET.Element(f'{{{NS}}}PageContents', attrib={'xml:space': 'preserve'})
    shapes_el = ET.SubElement(page, f'{{{NS}}}Shapes')

    sid_counter = [0]
    def nid():
        sid_counter[0] += 1
        return sid_counter[0]

    # ─── Title bar ───────────────────────────────────────────────────────────
    sid = nid()
    shapes_el.append(make_label_shape(
        sid, 5.5, 10.5, 9.0, 0.55,
        '高校科研项目申报与管理系统 - 项目架构图', '#1a237e'))

    # ─── Layer labels (left side) ────────────────────────────────────────────
    layers = [
        (1.1, 9.2, '前端层\nVue3 + Element Plus', '#1565c0'),
        (1.1, 6.8, 'API 层\nDjango REST Framework', '#2e7d32'),
        (1.1, 4.4, '后端层\nDjango Apps', '#e65100'),
        (1.1, 2.0, '数据层\nMySQL', '#6a1b9a'),
    ]
    for _, lx, lt, lc in layers:
        shapes_el.append(make_label_shape(nid(), lx, lt.split('\n')[1] if '\n' in lt else lt,
                                          1.5, 1.3, lt, lc))

    # ─── Frontend components ─────────────────────────────────────────────────
    fe_items = [
        (3.3, 9.8, 1.1, 0.7, 'Login.vue\n登录页', '#42a5f5'),
        (4.7, 9.8, 1.2, 0.7, 'Dashboard.vue\n项目列表', '#42a5f5'),
        (6.2, 9.8, 1.1, 0.7, 'Apply.vue\n项目申报', '#42a5f5'),
        (7.55, 9.8, 1.15, 0.7, 'Review.vue\n审核中心', '#42a5f5'),
        (3.85, 8.8, 1.05, 0.55, 'auth.js\n登录API', '#90caf9'),
        (5.3, 8.8, 1.05, 0.55, 'project.js\n项目API', '#90caf9'),
        (6.75, 8.8, 1.2, 0.55, 'request.js\nAxios+JWT拦截器', '#90caf9'),
        (5.3, 7.8, 1.05, 0.55, 'router/index.js\n路由守卫(RBAC)', '#90caf9'),
    ]
    for fx, fy, fw, fh, ft, fc in fe_items:
        shapes_el.append(make_label_shape(nid(), fx, fy, fw, fh, ft, fc))

    # ─── API endpoints ───────────────────────────────────────────────────────
    api_items = [
        (3.3, 7.2, 1.1, 0.7, '/api/login/\nJWT认证', '#66bb6a'),
        (4.7, 7.2, 1.2, 0.7, '/api/projects/\n项目CRUD+审核', '#66bb6a'),
        (6.2, 7.2, 1.1, 0.7, '/api/register/\n用户注册', '#66bb6a'),
        (7.55, 7.2, 1.15, 0.7, '/api/user/info/\n用户信息', '#66bb6a'),
        (5.3, 6.3, 1.4, 0.55, 'settings.py\nJWT+CORS+分页配置', '#a5d6a7'),
        (6.75, 6.3, 1.2, 0.55, 'urls.py\n路由配置', '#a5d6a7'),
    ]
    for ax, ay, aw, ah, at, ac in api_items:
        shapes_el.append(make_label_shape(nid(), ax, ay, aw, ah, at, ac))

    # ─── Backend apps ────────────────────────────────────────────────────────
    be_items = [
        (3.3, 4.8, 1.55, 0.95, 'apps/users/\nmodels.py\nserializers.py\nviews.py\nurls.py', '#ff9800'),
        (5.3, 4.8, 1.55, 0.95, 'apps/projects/\nmodels.py\nserializers.py\nviews.py\nurls.py', '#ff9800'),
        (7.3, 4.8, 1.55, 0.95, 'research_system/\nsettings.py\nurls.py\nwsgi.py', '#ff9800'),
        (4.3, 3.8, 1.2, 0.55, 'manage.py\nDjango入口', '#ffcc80'),
        (6.3, 3.8, 1.2, 0.55, 'init_data.py\n初始化脚本', '#ffcc80'),
    ]
    for bx, by, bw, bh, bt, bc in be_items:
        shapes_el.append(make_label_shape(nid(), bx, by, bw, bh, bt, bc))

    # ─── Database tables ─────────────────────────────────────────────────────
    db_items = [
        (3.3, 2.4, 1.55, 0.75, 'auth_user\n用户表\n(admin/teacher/expert)', '#7b1fa2'),
        (5.3, 2.4, 1.55, 0.75, 'research_projects\n项目表\n(pending/approved/rejected)', '#7b1fa2'),
        (7.3, 2.4, 1.55, 0.75, 'project_reviews\n审核记录表', '#7b1fa2'),
    ]
    for dx, dy, dw, dh, dt, dc in db_items:
        shapes_el.append(make_label_shape(nid(), dx, dy, dw, dh, dt, dc))

    # ─── Right side: other modules ───────────────────────────────────────────
    side_items = [
        (9.6, 9.5, 2.2, 0.85, 'Django-Management web/\nVue3 前端项目', '#00bcd4'),
        (9.6, 7.8, 2.2, 1.05, 'work/work/\nDjango模板版本\n(Student/Teacher/Admin)\n完整功能实现', '#00bcd4'),
        (9.6, 5.8, 2.2, 0.85, 'DjangoProject/\n原始Django项目', '#0097a7'),
        (9.6, 4.2, 2.2, 0.85, '需求文档.md\n启动说明.md\nprojectSql.md', '#80deea'),
    ]
    for sx, sy, sw, sh, st, sc in side_items:
        shapes_el.append(make_label_shape(nid(), sx, sy, sw, sh, st, sc))

    # ─── Connector arrows ────────────────────────────────────────────────────
    # Frontend -> API (vertical connections)
    conns = [
        (3.85, 9.45, 3.85, 7.55),   # auth.js -> /api/login/
        (5.3, 9.45, 5.3, 7.55),     # project.js -> /api/projects/
        (6.75, 9.45, 6.75, 7.55),   # request.js -> /api/register/
        (3.3, 9.1, 3.3, 7.9),       # Login.vue -> api area
        (7.55, 9.1, 7.55, 7.9),     # Review.vue -> api area
        # API -> Backend
        (3.85, 6.85, 3.85, 5.25),   # /api/login/ -> apps/users
        (5.3, 6.85, 5.3, 5.25),     # /api/projects/ -> apps/projects
        (6.75, 6.85, 6.75, 5.25),   # /api/register/ -> apps/users
        # Backend -> DB
        (3.3, 4.25, 3.3, 2.8),      # apps/users -> auth_user
        (5.3, 4.25, 5.3, 2.8),      # apps/projects -> research_projects
        (7.3, 4.25, 7.3, 2.8),      # research_system -> project_reviews
        # Side connections
        (8.85, 9.8, 9.05, 9.9),     # Frontend area -> side module
        (8.85, 5.3, 9.05, 6.2),     # Backend -> side
    ]
    for bx, by, ex, ey in conns:
        shapes_el.append(make_connector(nid(), bx, by, ex, ey))

    # ─── Assemble the new VSDX ───────────────────────────────────────────────
    page_xml_str = serialize_xml(page)

    new_files = dict(template_files)
    new_files['visio/pages/page1.xml'] = page_xml_str.encode('utf-8')

    print(f"Writing {OUT_VSDX}...")
    with zipfile.ZipFile(OUT_VSDX, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in new_files.items():
            zout.writestr(name, data)

    print(f"Done! Total shapes: {sid_counter[0]}")


if __name__ == '__main__':
    generate()
