// ------------------------------------------------------------
// MAK 2026
// miladasgarpour@gmail.com
//          Treat all numbers in mm 
//          3D printer in 22 cm by 22 cm 
// ------------------------------------------------------------
// ============================================================
// 
//                      Soap Holder: Start
//
holder_length = 100; 
holder_width = 65;
holder_height = 10;
corner_radius = 25;
wall_thickness = 2.5; 
base_thickness = 2.0;
top_thickness = 1.5; 
tolerance = 0.25; 
hex_radius = 2.5;
hex_wall = 1.5; 
border_width = 2.5;
notch_width = 15.0;        
notch_depth = 1.5; 
snap_lock_enabled = true;
tab_width = notch_width - 0.5;
tab_projection = 2.0;
tab_thickness = 1.5;
tab_clearance = 0.25;
module pill_shape(l, w, r) {
    hull() {
        translate([-(l/2 - r), -(w/2 - r), 0]) circle(r=r, $fn=64);
        translate([ (l/2 - r), -(w/2 - r), 0]) circle(r=r, $fn=64);
        translate([-(l/2 - r),  (w/2 - r), 0]) circle(r=r, $fn=64);
        translate([ (l/2 - r),  (w/2 - r), 0]) circle(r=r, $fn=64);
    }
}
module honeycomb_grid(l, w, r, hex_r, wall_t, b_width) {
    dx = sqrt(3) * hex_r + wall_t;
    dy = 1.5 * hex_r + (wall_t * sqrt(3)/2); 
    nx = ceil(l / dx) + 2;
    ny = ceil(w / dy) + 2;
    intersection() {
        pill_shape(l - 2*b_width, w - 2*b_width, max(1, r - b_width));
        union() {
            for (xi = [-nx:nx]) {
                for (yi = [-ny:ny]) {
                    x_offset = (yi % 2 != 0) ? dx / 2 : 0;
                    x_pos = xi * dx + x_offset;
                    y_pos = yi * dy;
                    
                    if (abs(x_pos) < l/2 && abs(y_pos) < w/2) {
                        translate([x_pos, y_pos, 0])
                            rotate([0, 0, 30])
                                circle(r=hex_r, $fn=6);
                    }
                }
            }
        }
    }
}
module holder_part() {
    difference() {
        linear_extrude(height = holder_height)
            pill_shape(holder_length, holder_width, corner_radius);
        translate([0, 0, base_thickness])
            linear_extrude(height = holder_height - base_thickness + 1)
                pill_shape(holder_length - 2*wall_thickness, holder_width - 
                    2*wall_thickness, max(1, corner_radius - wall_thickness));
                
        translate([0, 0, holder_height - top_thickness])
            linear_extrude(height = top_thickness + 1)
                pill_shape(holder_length - 2*wall_thickness + 1.2*wall_thickness, 
                    holder_width - 2*wall_thickness + 1.2*wall_thickness, 
                        max(1, corner_radius - wall_thickness/2));

        for (side = [-1, 1]) {
            translate([0, side * (holder_width/2), holder_height - notch_depth/2])
                cube([notch_width, wall_thickness * 4, notch_depth], center=true);
        }
    }
}
module top_part() {
    effective_l = holder_length - wall_thickness - tolerance;
    effective_w = holder_width - wall_thickness - tolerance;
    effective_r = max(1, corner_radius - wall_thickness - tolerance/2);
    difference() {
        union() {
            linear_extrude(height = top_thickness)
                pill_shape(
                    effective_l,
                    effective_w,
                    effective_r
                );
            if (snap_lock_enabled) {
                for (side = [-1, 1]) {
                    translate([
                        0,
                        side * (effective_w/2 + tab_projection/2),
                        top_thickness/2 + 0.2
                    ])
                    cube([
                        tab_width - tab_clearance,
                        tab_projection,
                        tab_thickness
                    ], center = true);
                }
            }
        }
        translate([0, 0, -1])
            linear_extrude(height = top_thickness + 2)
                honeycomb_grid(
                    effective_l,
                    effective_w,
                    effective_r,
                    hex_radius,
                    hex_wall,
                    border_width
                );
    }
}
module render_assembly() {
    if (part_to_render == "both" || part_to_render == "holder") {
        translate([0, 0, 0]) holder_part();
    }
    if (part_to_render == "both" || part_to_render == "top") {
        translate([holder_length + 20, 0, 0]) top_part();
    }
}
// 
// comment out next two lines to render 
part_to_render = "both";   // Options: "both", "holder", "top"
render_assembly();        
//
//                      Soap Holder: End
// 
// ============================================================