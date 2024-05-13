#version 330

in vec3 in_position;
uniform mat4 pvm;

void main() {
    gl_Position = pvm * vec4(in_position, 1.0);
}