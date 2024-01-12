#version 330

in vec3 frag_color;
out vec4 color;

void main() {
    color = vec4(frag_color.r, frag_color.g, frag_color.b, 1.0);
}