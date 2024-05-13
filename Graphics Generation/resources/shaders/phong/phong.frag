#version 330

out vec4 f_color;

in vec3 position;
in vec3 normal;

uniform vec3 view_position;
uniform vec3 obj_color;

uniform vec3 light_position;
uniform vec3 light_color;

uniform float shininess_param;
uniform float ambient_param;
uniform float specular_param;
uniform float diffuse_param;

void main() {
    // the change due to ambient part of the equation
    vec3 ambient = ambient_param * light_color;

    // due to diffuse part
    vec3 light_direction = normalize(light_position - position);
    vec3 diffuse = diffuse_param * max(dot(normal, light_direction), 0.0) * light_color;

    // due to specular part
    vec3 view_direction = normalize(view_position - position);
    vec3 refl_direction= reflect(-light_direction, normal);
    vec3 specular = specular_param * pow(max(dot(view_direction, refl_direction), 0.0), shininess_param) * light_color;

    // sum of all the above parts is the matrix to apply
    vec3 phong_shading = (ambient + diffuse + specular) * obj_color;

    // the result of Phong shading
    f_color = vec4(phong_shading, 1.0);
}
