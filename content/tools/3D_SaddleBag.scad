// ------------------------------------------------------------
// MAK 2026
// miladasgarpour@gmail.com
//          Treat all numbers in mm 
//          3D printer in 22 cm by 22 cm 
// ------------------------------------------------------------
// ============================================================
// 
//                      Saddle Bag: Start
// 
$fn = 68;  
width_scale  = 0.5; 
height_scale = 0.75;
base_height  = 165; 
base_width   = 65;
bag_length   = 125;
lid_height   = 22;
wall         = 2.5;
z_bottom     = 5;
slice_step   = 6;
bag_height   = base_height * height_scale;
bag_width    = base_width  * width_scale;
z_lid        = bag_height - lid_height;
height_shift = bag_height - base_height;
front_tbl = [[5,-8],[35,-8],[60,-3],[100,-1],[165,0]];                                 
rear_tbl  = [[5,8],[10,8],[35,35],[60,68],[85,100],[108,124],[165,124]];               
width_tbl = [[5,14],[10,16],[35,26],[60,40],[108,60],[165,62]];                        
function x_front(z) = lookup(z / height_scale, front_tbl);               
function x_rear(z)  = lookup(z / height_scale, rear_tbl);                
function y_width(z) = width_scale * lookup(z / height_scale, width_tbl); 
module slab(z, inset = 0, h = 0.01) { 
    x0 = x_front(z) + inset; 
    x1 = x_rear(z)  - inset; 
    w  = y_width(z) - 2 * inset;
    r  = max(0.5, min(14, w / 2 - 0.3, (x1 - x0) / 2 - 0.3));   
    translate([0, 0, z]) 
    linear_extrude(height = h) 
    offset(r = r) 
    translate([x0 + r, -w / 2 + r]) 
    square([max(0.1, x1 - x0 - 2 * r),
            max(0.1, w - 2 * r)]); 
}
module loft(z_start, z_end, inset = 0) { 
    n = ceil((z_end - z_start) / slice_step);
    for (i = [0 : n - 1]) { 
        za = z_start + i * (z_end - z_start) / n;
        zb = z_start + (i + 1) * (z_end - z_start) / n; 
        hull() { 
            slab(za, inset); 
            slab(zb, inset); 
        } 
    }   
}  
module body() { 
    difference() {   
        loft(z_bottom, z_lid + 0.5, 0);  
        loft(z_bottom + wall, z_lid + 2, wall); 
    }
} 
module lid_solid(inset = 0) {
    hull() { 
        slab(z_lid,       inset - 1.0); 
        slab(z_lid + 14,  inset - 1.0); 
        slab(z_lid + 20,  inset + 3.0);
        slab(bag_height - 0.5 - inset, inset + 6.0);
    }  
} 
module lid() { 
    difference() {   
        lid_solid(0); 
        lid_solid(wall);
        translate([0, 0, z_lid - 1]) 
            linear_extrude(2)  
            translate([x_front(z_lid) + wall, -y_width(z_lid) / 2 + wall]) 
            square([x_rear(z_lid) - x_front(z_lid) - 2 * wall,
                    y_width(z_lid) - 2 * wall]); 
    } 
}  
module rear_tab() {
    translate([x_rear(z_lid) - 3, 0, height_shift]) 
    rotate([90, 0, 0]) 
    linear_extrude(height = 3, center = true) 
    difference() { 
        polygon([[0, 129], [12, 131], [12, 147], [0, 149]]);
        translate([7, 134]) circle(d = 3.4);   
        translate([7, 143]) circle(d = 3.4); 
    }  
}  
module foot_tab() {   
    translate([0, 0, 0])  
    rotate([90, 0, 0])  
    linear_extrude(height = 3, center = true)  
    difference() {  
        polygon([[-3, 34], [-22, 20], [-22, 8], [-6, 6], [-3, 12]]);  
        translate([-17.5, 12.5]) square(3.5, center = true); 
    }    
}    
// comment out next four lines to render 
//body();                                // add the hollow wedge body
//lid();                                 // add the lid cap on top
//rear_tab();                            // add the two-hole rear tab
//foot_tab();                            // add the bottom slotted foot tab
// 
//                      Saddle Bag: End 
//
// ============================================================