# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ----------------------------- 辅助函数 -----------------------------
def add_single_thermocouple(ax, side, left_dist, right_dist, width, height, a_center_y,
                            total_length, boss_width, text_offset=10):
    """
    在已有的 ax 上添加指定侧的电偶及其尺寸标注。
    参数：
        side: 'left' 或 'right'
        left_dist: 左侧电偶距离整体左边框的距离 (mm)
        right_dist: 右侧电偶距离凸台左侧的距离 (mm)
        width: 电偶宽度 (mm)
        height: 电偶高度 (mm)
        a_center_y: A区中心 y 坐标 (mm)
        total_length: 主体总长 (mm)
        boss_width: 右侧凸台宽度 (mm)
        text_offset: 尺寸标注文字偏移量 (mm)
    """
    arrowprops = dict(arrowstyle='<->', color='black', lw=0.8)

    def draw_extension_line(x_start, y_start, x_end, y_end):
        ax.plot([x_start, x_end], [y_start, y_end], color='black', linewidth=0.5, linestyle='-')

    if side == 'left':
        x0 = left_dist
        y0 = a_center_y
        # 绘制橙色矩形
        rect = patches.Rectangle((x0, y0), width, height,
                                 linewidth=0.5, edgecolor='red', facecolor='orange')
        ax.add_patch(rect)

        # 高度标注 (放在电偶右侧)
        x_dim = x0 + width + text_offset
        y_bottom = y0
        y_top = y0 + height
        ax.annotate('', xy=(x_dim, y_bottom), xytext=(x_dim, y_top), arrowprops=arrowprops)
        ax.text((x0 + width + x_dim) / 2, (y_bottom + y_top) / 2, f'{height:.1f}',
                ha='center', va='center', color='black', rotation=90)
        draw_extension_line(x0 + width, y_bottom, x_dim, y_bottom)
        draw_extension_line(x0 + width, y_top, x_dim, y_top)

        # 距离标注 (电偶左侧到整体左边框)
        y_dim = y_bottom + 5
        ax.annotate('', xy=(0, y_dim), xytext=(x0, y_dim), arrowprops=arrowprops)
        ax.text((0 + x0) / 2, y_dim + 2, f'{left_dist}', ha='center', va='bottom', color='black')
        draw_extension_line(0, y_bottom, 0, y_dim)
        draw_extension_line(x0, y_bottom, x0, y_dim)

    elif side == 'right':
        x0 = total_length - right_dist - width
        y0 = a_center_y
        rect = patches.Rectangle((x0, y0), width, height,
                                 linewidth=0.5, edgecolor='red', facecolor='orange')
        ax.add_patch(rect)

        # 高度标注 (放在电偶左侧)
        x_dim = x0 - text_offset
        y_bottom = y0
        y_top = y0 + height
        ax.annotate('', xy=(x_dim, y_bottom), xytext=(x_dim, y_top), arrowprops=arrowprops)
        ax.text((x0 + x_dim) / 2, (y_bottom + y_top) / 2, f'{height:.1f}',
                ha='center', va='center', color='black', rotation=90)
        draw_extension_line(x0, y_bottom, x_dim, y_bottom)
        draw_extension_line(x0, y_top, x_dim, y_top)

        # 距离标注 (电偶右侧到凸台左侧)
        y_dim = y_bottom + 5
        ax.annotate('', xy=(x0 + width, y_dim), xytext=(total_length, y_dim), arrowprops=arrowprops)
        ax.text((x0 + width + total_length) / 2, y_dim + 2, f'{right_dist}', ha='center', va='bottom', color='black')
        draw_extension_line(x0 + width, y_bottom, x0 + width, y_dim)
        draw_extension_line(total_length, y_bottom, total_length, y_dim)

    # 调整 y 轴范围以包含电偶顶部
    current_ylim = ax.get_ylim()
    new_top = max(current_ylim[1], y_top + 30)
    new_bottom = min(current_ylim[0], y_bottom - 30)
    ax.set_ylim(bottom=new_bottom, top=new_top)


# ----------------------------- 主绘图函数 -----------------------------
def draw_wing_schematic(
    widths,
    wing_span,               # mm
    total_length=500,
    bottom_height=72.5,
    top_height=72.5,
    boss_width=10,
    left_boss_width=10,
    hole_diameter=6,
    hole_positions_y=None,   # 可选的圆孔 y 坐标列表
    show_thermocouple=False,
    thermocouple_side='left',
    thermocouple_width=7,
    thermocouple_extension=10,
    left_thermocouple_dist=20,
    right_thermocouple_dist=10,
    dpi=100
):
    """
    绘制主机翼防冰分区设计图。

    参数：
        widths: dict, 包含 'C','B','A','D','E' 五个区的高度 (mm)
        wing_span: 翼展单边长度 (mm)，用于底部总长标注
        total_length: 图形主体总长 (mm)，默认 500
        bottom_height: 底部段高度 (mm)，默认 72.5
        top_height: 顶部段高度 (mm)，默认 72.5
        boss_width: 右侧凸台宽度 (mm)，默认 10
        left_boss_width: 左侧黄色矩形宽度 (mm)，默认 10
        hole_diameter: 圆孔直径 (mm)，默认 6
        hole_positions_y: 圆孔中心的 y 坐标列表 (mm)，若为 None 则使用默认值
        show_thermocouple: 是否绘制电偶
        thermocouple_side: 电偶位置，'left' 或 'right'
        thermocouple_width: 电偶宽度 (mm)
        thermocouple_extension: 电偶超出顶部段上边界的距离 (mm)
        left_thermocouple_dist: 左侧电偶距离整体左边框的距离 (mm)
        right_thermocouple_dist: 右侧电偶距离凸台左侧的距离 (mm)
        dpi: 图形分辨率

    返回：
        matplotlib.figure.Figure 对象
    """
    # 从字典中提取各区高度
    step1_height = widths.get('C', 0)
    step2_height = widths.get('B', 0)
    step3_height = widths.get('A', 0)
    step4_height = widths.get('D', 0)
    step5_height = widths.get('E', 0)

    # 计算各关键 y 坐标
    bottom_y = -bottom_height
    step1_y = 0
    step2_y = step1_y + step1_height
    step3_y = step2_y + step2_height
    step4_y = step3_y + step3_height
    step5_y = step4_y + step4_height
    top_y = step5_y + step5_height
    top_end_y = top_y + top_height

    boss_right_x = total_length + boss_width

    # A 区中心 y 坐标（用于电偶起始点）
    a_center_y = (step3_y + step4_y) / 2

    # 电偶高度
    base_height_to_top = top_end_y - a_center_y
    thermocouple_height = base_height_to_top + thermocouple_extension

    # 创建画布
    fig, ax = plt.subplots(figsize=(14, 8), dpi=dpi)
    ax.set_aspect('equal')
    ax.set_xlim(-20, boss_right_x + 60)
    # y 轴范围留出足够空间
    y_min = bottom_y - 30
    y_max = top_end_y + 40 + (thermocouple_extension if show_thermocouple else 0)
    ax.set_ylim(y_min, y_max)
    ax.axis('off')

    # 定义颜色
    color_gray_light = '#d3d3d3'
    color_yellow = '#FFFF00'
    plt.rcParams['hatch.linewidth'] = 0.2

    # ========== 绘制所有矩形（边框红色） ==========
    rectangles = [
        # 底部段
        (0, bottom_y, total_length, bottom_height, color_gray_light),
        # 第一台阶 C 区
        (0, step1_y, total_length, step1_height, 'white'),
        # 第二台阶 B 区
        (0, step2_y, total_length, step2_height, 'white'),
        # 第三台阶 A 区
        (0, step3_y, total_length, step3_height, 'white'),
        # 第四台阶 D 区
        (0, step4_y, total_length, step4_height, 'white'),
        # 第五台阶 E 区
        (0, step5_y, total_length, step5_height, 'white'),
        # 顶部段
        (0, top_y, total_length, top_height, color_gray_light),
        # 右侧凸台上段
        (total_length, top_y, boss_width, top_height, color_yellow),
        # 右侧凸台下段
        (total_length, bottom_y, boss_width, bottom_height, color_yellow),
        # 左侧黄色上矩形
        (0, top_y, left_boss_width, top_height, color_yellow),
        # 左侧黄色下矩形
        (0, bottom_y, left_boss_width, bottom_height, color_yellow),
    ]
    for x, y, w, h, fc in rectangles:
        rect = patches.Rectangle((x, y), w, h, linewidth=0.5, edgecolor='red', facecolor=fc)
        ax.add_patch(rect)

    # ========== 绘制圆孔 ==========
    if hole_positions_y is None:
        # 默认圆孔位置（与原始 1.1.py 一致）
        hole_positions_y = [-67.5, -57.5, -47.5, -37.5, -27.5, -17.5, -7.5,
                            85, 95, 105, 115, 125, 135, 145]
    hole_radius = hole_diameter / 2
    hole_x = total_length + boss_width / 2
    for y in hole_positions_y:
        circle = patches.Circle((hole_x, y), radius=hole_radius, linewidth=0.5,
                                edgecolor='red', facecolor='white')
        ax.add_patch(circle)

    # ========== 绘制填充图案（斜线/反斜线） ==========
    hatch1_rects = [
        (0, step1_y, total_length, step1_height),
        (0, step3_y, total_length, step3_height),
        (0, step5_y, total_length, step5_height),
        (total_length, top_y, boss_width, top_height),
        (total_length, bottom_y, boss_width, bottom_height),
        (0, top_y, left_boss_width, top_height),
        (0, bottom_y, left_boss_width, bottom_height),
    ]
    hatch2_rects = [
        (0, step2_y, total_length, step2_height),
        (0, step4_y, total_length, step4_height),
    ]
    for x, y, w, h in hatch1_rects:
        rect = patches.Rectangle((x, y), w, h, fill=False, hatch='//', edgecolor='red', linewidth=0)
        ax.add_patch(rect)
    for x, y, w, h in hatch2_rects:
        rect = patches.Rectangle((x, y), w, h, fill=False, hatch='\\\\', edgecolor='red', linewidth=0)
        ax.add_patch(rect)

    # ========== 尺寸标注 ==========
    arrowprops = dict(arrowstyle='<->', color='black', lw=0.8)
    text_offset = 10

    def draw_extension_line(x_start, y_start, x_end, y_end):
        ax.plot([x_start, x_end], [y_start, y_end], color='black', linewidth=0.5, linestyle='-')

    # 1. 底部总长标注（显示实际翼展长度）
    y_bottom_dim = bottom_y - text_offset
    ax.annotate('', xy=(0, y_bottom_dim), xytext=(total_length, y_bottom_dim),
                arrowprops=arrowprops)
    ax.text(total_length / 2, (bottom_y + y_bottom_dim) / 2, f'{wing_span:.0f}',
            ha='center', va='center', color='black')
    draw_extension_line(0, bottom_y, 0, y_bottom_dim)
    draw_extension_line(total_length, bottom_y, total_length, y_bottom_dim)

    # 2. 总高标注（左侧）
    left_x = -text_offset
    ax.annotate('', xy=(left_x, bottom_y), xytext=(left_x, top_end_y),
                arrowprops=arrowprops)
    total_height = top_end_y - bottom_y
    ax.text((left_x + 0) / 2, (bottom_y + top_end_y) / 2, f'{total_height:.0f}',
            ha='center', va='center', color='black', rotation=90)
    draw_extension_line(0, bottom_y, left_x, bottom_y)
    draw_extension_line(0, top_end_y, left_x, top_end_y)

    # 3. 右侧凸台宽度标注
    y_boss_dim = top_y + text_offset
    ax.annotate('', xy=(total_length, y_boss_dim), xytext=(boss_right_x, y_boss_dim),
                arrowprops=arrowprops)
    ax.text(total_length + boss_width / 2, (top_y + y_boss_dim) / 2, f'{boss_width}',
            ha='center', va='center', color='black')
    draw_extension_line(total_length, top_y, total_length, y_boss_dim)
    draw_extension_line(boss_right_x, top_y, boss_right_x, y_boss_dim)

    # 4. 左侧黄色矩形宽度标注
    y_left_boss_dim = top_y + text_offset
    ax.annotate('', xy=(0, y_left_boss_dim), xytext=(left_boss_width, y_left_boss_dim),
                arrowprops=arrowprops)
    ax.text(left_boss_width / 2, (top_y + y_left_boss_dim) / 2, f'{left_boss_width}',
            ha='center', va='center', color='black')
    draw_extension_line(0, top_y, 0, y_left_boss_dim)
    draw_extension_line(left_boss_width, top_y, left_boss_width, y_left_boss_dim)

    # 5. 顶部总宽标注（从左边框到凸台右边框）
    y_top_dim = top_end_y + 2 * text_offset
    ax.annotate('', xy=(0, y_top_dim), xytext=(boss_right_x, y_top_dim),
                arrowprops=arrowprops)
    ax.text(boss_right_x / 2, (top_end_y + y_top_dim) / 2, f'{boss_right_x}',
            ha='center', va='center', color='black')
    draw_extension_line(0, top_end_y, 0, y_top_dim)
    draw_extension_line(boss_right_x, top_end_y, boss_right_x, y_top_dim)

    # 6. 右侧分段高度标注（各台阶高度 + 底部/顶部段）
    # 为避免与凸台重叠，将标注线向右移动至凸台右侧
    right_dim_x = total_length + boss_width + 2 * text_offset
    right_dim_x1 = total_length + boss_width  # 用于台阶标注，缩短引线

    # 底部段高度
    y1, y2 = bottom_y, step1_y
    ax.annotate('', xy=(right_dim_x, y1), xytext=(right_dim_x, y2), arrowprops=arrowprops)
    ax.text((total_length + right_dim_x) / 2 + text_offset, (y1 + y2) / 2, f'{bottom_height}',
            ha='center', va='center', color='black', rotation=90)
    draw_extension_line(total_length, y1, right_dim_x, y1)
    draw_extension_line(total_length, y2, right_dim_x, y2)

    # 第一台阶
    y1, y2 = step1_y, step2_y
    ax.annotate('', xy=(right_dim_x1, y1), xytext=(right_dim_x1, y2), arrowprops=arrowprops)
    ax.text((total_length + right_dim_x) / 2, (y1 + y2) / 2, f'{step1_height}',
            ha='center', va='center', color='black', rotation=90)
    draw_extension_line(total_length, y1, right_dim_x1, y1)
    draw_extension_line(total_length, y2, right_dim_x1, y2)

    # 第二台阶
    y1, y2 = step2_y, step3_y
    ax.annotate('', xy=(right_dim_x1, y1), xytext=(right_dim_x1, y2), arrowprops=arrowprops)
    ax.text((total_length + right_dim_x) / 2, (y1 + y2) / 2, f'{step2_height}',
            ha='center', va='center', color='black', rotation=90)
    draw_extension_line(total_length, y1, right_dim_x1, y1)
    draw_extension_line(total_length, y2, right_dim_x1, y2)

    # 第三台阶
    y1, y2 = step3_y, step4_y
    ax.annotate('', xy=(right_dim_x1, y1), xytext=(right_dim_x1, y2), arrowprops=arrowprops)
    ax.text((total_length + right_dim_x) / 2, (y1 + y2) / 2, f'{step3_height}',
            ha='center', va='center', color='black', rotation=90)
    draw_extension_line(total_length, y1, right_dim_x1, y1)
    draw_extension_line(total_length, y2, right_dim_x1, y2)

    # 第四台阶
    y1, y2 = step4_y, step5_y
    ax.annotate('', xy=(right_dim_x1, y1), xytext=(right_dim_x1, y2), arrowprops=arrowprops)
    ax.text((total_length + right_dim_x) / 2, (y1 + y2) / 2, f'{step4_height}',
            ha='center', va='center', color='black', rotation=90)
    draw_extension_line(total_length, y1, right_dim_x1, y1)
    draw_extension_line(total_length, y2, right_dim_x1, y2)

    # 第五台阶
    y1, y2 = step5_y, top_y
    ax.annotate('', xy=(right_dim_x1, y1), xytext=(right_dim_x1, y2), arrowprops=arrowprops)
    ax.text((total_length + right_dim_x) / 2, (y1 + y2) / 2, f'{step5_height}',
            ha='center', va='center', color='black', rotation=90)
    draw_extension_line(total_length, y1, right_dim_x1, y1)
    draw_extension_line(total_length, y2, right_dim_x1, y2)

    # 顶部段高度
    y1, y2 = top_y, top_end_y
    ax.annotate('', xy=(right_dim_x, y1), xytext=(right_dim_x, y2), arrowprops=arrowprops)
    ax.text((total_length + right_dim_x) / 2 + text_offset, (y1 + y2) / 2, f'{top_height}',
            ha='center', va='center', color='black', rotation=90)
    draw_extension_line(total_length, y1, right_dim_x, y1)
    draw_extension_line(total_length, y2, right_dim_x, y2)

    # ========== 添加颜色图例 ==========
    legend_x = boss_right_x + 70
    legend_y = top_end_y - 50
    legend_size = 15
    ax.add_patch(patches.Rectangle((legend_x, legend_y), legend_size, legend_size,
                                   facecolor=color_gray_light, edgecolor='red', linewidth=0.5))
    ax.add_patch(patches.Rectangle((legend_x, legend_y - 20), legend_size, legend_size,
                                   facecolor=color_yellow, edgecolor='red', linewidth=0.5))
    ax.add_patch(patches.Rectangle((legend_x, legend_y - 40), legend_size, legend_size,
                                   facecolor='white', edgecolor='red', linewidth=0.5, hatch='//'))
    ax.add_patch(patches.Rectangle((legend_x, legend_y - 60), legend_size, legend_size,
                                   facecolor='white', edgecolor='red', linewidth=0.5, hatch='\\\\'))
    # # 图例文字
    # ax.text(legend_x + legend_size + 5, legend_y + legend_size/2, "基体 (铝)", va='center')
    # ax.text(legend_x + legend_size + 5, legend_y - 20 + legend_size/2, "加热区 (铜)", va='center')
    # ax.text(legend_x + legend_size + 5, legend_y - 40 + legend_size/2, "防冰涂层 (疏水)", va='center')
    # ax.text(legend_x + legend_size + 5, legend_y - 60 + legend_size/2, "防冰涂层 (不疏水)", va='center')

    # ========== 添加电偶 ==========
    if show_thermocouple:
        add_single_thermocouple(
            ax=ax,
            side=thermocouple_side,
            left_dist=left_thermocouple_dist,
            right_dist=right_thermocouple_dist,
            width=thermocouple_width,
            height=thermocouple_height,
            a_center_y=a_center_y,
            total_length=total_length,
            boss_width=boss_width,
            text_offset=10
        )

    plt.tight_layout()
    return fig


# ----------------------------- 示例（测试用） -----------------------------
if __name__ == "__main__":
    # 示例参数
    test_widths = {
        'C': 25,
        'B': 10,
        'A': 10,
        'D': 10,
        'E': 25
    }
    # 生成无电偶图
    fig = draw_wing_schematic(test_widths, wing_span=4900, show_thermocouple=False)
    fig.savefig("无电偶.png", dpi=300, bbox_inches='tight')
    plt.close(fig)

    # 生成左电偶图
    fig = draw_wing_schematic(test_widths, wing_span=4900, show_thermocouple=True,
                              thermocouple_side='left', thermocouple_extension=10,
                              left_thermocouple_dist=20)
    fig.savefig("左电偶.png", dpi=300, bbox_inches='tight')
    plt.close(fig)

    # 生成右电偶图
    fig = draw_wing_schematic(test_widths, wing_span=4900, show_thermocouple=True,
                              thermocouple_side='right', thermocouple_extension=10,
                              right_thermocouple_dist=10)
    fig.savefig("右电偶.png", dpi=300, bbox_inches='tight')
    plt.close(fig)