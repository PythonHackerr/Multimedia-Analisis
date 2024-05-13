#version 330

out vec4 f_color;
uniform vec3 col;

void main()
{
    f_color = vec4(normalize(col), 1.0);
}
