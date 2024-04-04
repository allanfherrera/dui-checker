#Library to validate Salvadoran ID´s
# Implemented in Python GTK 3

# Copyright (C) 2023 Allan Herrera
# This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation
# either version 2.1 of the License, or (at your option) any later version.
#This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.
#You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

def validar_dui(dui):
    """
    Valida si un número de DUI (Documento Único de Identidad) de El Salvador es válido.

    Parámetros:
    dui (str): Número de DUI a validar.

    Retorna:
    bool: True si el DUI es válido, False de lo contrario.
    """

    # Inicialización de variables
    resultadoValidacion = True
    checksum = 0
    valor = 9
    digito_verificador = 0

    try:
        # Verifica la longitud del DUI
        if len(dui) != 9:
            resultadoValidacion = False
        else:
            # Verifica que todos los caracteres sean dígitos
            for digito in dui:
                if not digito.isdigit():
                    resultadoValidacion = False
                    break

            # Si todos los caracteres son dígitos
            if resultadoValidacion:
                # Calcula el checksum
                for i in range(1, 9):
                    checksum += int(dui[i - 1]) * valor
                    valor -= 1

                # Calcula el dígito verificador
                resto = checksum % 10
                resta = 10 - resto if resto != 0 else 0

                # Verifica si el dígito verificador coincide con el último dígito del DUI
                if resta != int(dui[8]):
                    resultadoValidacion = False

    except ValueError:
        # Se atrapó una excepción al intentar convertir un caracter a int
        resultadoValidacion = False

    return resultadoValidacion

class CuadroValidacionDUI(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Validar DUI", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(250, 200)

        box = self.get_content_area()

        self.entry = Gtk.Entry()
        box.add(Gtk.Label("Ingrese su número de DUI sin guiones:"))
        box.add(self.entry)
        self.show_all()

    def get_dui(self):
        return self.entry.get_text()

def main():
    dialog = CuadroValidacionDUI(None)
    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        dui_ingresado = dialog.get_dui()
        resultado = validar_dui(dui_ingresado)
        if resultado:
            mensaje = "El DUI ingresado es válido"
        else:
            mensaje = "El DUI ingresado es inválido"
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, mensaje)
        dialog.run()
        dialog.destroy()

    dialog.destroy()

if __name__ == "__main__":
    main()
