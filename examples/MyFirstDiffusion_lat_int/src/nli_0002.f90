module nli_0002
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_CO_diffusion_hollow1_right(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_CO_diffusion_hollow1_right

    select case(get_species(cell + (/0, 0, 0, simple_cubic_hollow1/)))
      case default
        nli_CO_diffusion_hollow1_right = 0; return
      case(CO)
        select case(get_species(cell + (/0, 0, 0, simple_cubic_hollow2/)))
          case default
            nli_CO_diffusion_hollow1_right = 0; return
          case(empty)
            nli_CO_diffusion_hollow1_right = CO_diffusion_hollow1_right; return
        end select
    end select

end function nli_CO_diffusion_hollow1_right

end module
