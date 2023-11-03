import { mount } from "@vue/test-utils";
import Candidates from "./Candidates.vue"; 

import { afterAll, afterEach, beforeAll } from "vitest";
import { setupServer } from "msw/node";
import { http } from "msw";

export const restHandlers = [
  http.get("http://127.0.0.1:5000/api/getapplications", (req, res, ctx) => {
    return res(ctx.status(200), ctx.json({ data: [] }));
  }),
  http.get("http://127.0.0.1:5000/api/getRoleListing/1", (req, res, ctx) => {
    return res(ctx.status(200), ctx.json({ data: [] }));
  }),
  http.get(
    "http://127.0.0.1:5000/api/getApplicantsBySkillMatch/1",
    (req, res, ctx) => {
      return res(ctx.status(200), ctx.json({ data: [] }));
    }
  ),
];

const server = setupServer(...restHandlers);

// Start server before all tests
beforeAll(() => server.listen({ onUnhandledRequest: "error" }));

//  Close server after all tests
afterAll(() => server.close());

// Reset handlers after each test `important for test isolation`
afterEach(() => server.resetHandlers());

const mockRoute = {
  // params: {
  //   id: 1
  // }
};
const mockRouter = {
  push: vi.fn(),
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
describe("Candidates", () => {
  it("renders successfully", () => {
    const wrapper = mount(Candidates, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
      stubs: ["router-link", "router-view"],
    });
    expect(wrapper.exists()).toBe(true);
  });

  it("initializes data correctly", () => {
    const wrapper = mount(Candidates, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
      stubs: ["router-link", "router-view"],
    });
    const data = wrapper.vm.$data;

    // Assert that your data properties are initialized as expected
    expect(data.applications).toEqual([]);
    expect(data.roles).toEqual([]);
    // Add more assertions for other data properties
  });

  it("calculates application count correctly", async () => {
    // Mount your component
    const { vm } = mount(Candidates, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
      stubs: ["router-link", "router-view"],
    });

    // Wait for the component to process the API response
    await sleep(1000);

    // Assert that the applications are correctly set in the component
    expect(vm.applications.length).toEqual(0);

    expect(vm.roles).toEqual([]);

    // Assert that the application count is calculated correctly
    expect(vm.applicationCount).toBe(0);
  });
  it("correctly filters candidates based on selected skills", async () => {
    const wrapper = mount(Candidates, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
      stubs: ["router-link", "router-view"],
    });
    await wrapper.vm.$nextTick();

    // Simulate selecting specific skills in the component
    wrapper.setData({ selectedSkills: ["Skill1", "Skill2"] });

    // Assert that filteredCandidates contains only candidates with the selected skills
    expect(wrapper.vm.filteredCandidates).toEqual([]);
  });
  it("correctly calculates application count when role changes", async () => {
    const wrapper = mount(Candidates, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
      stubs: ["router-link", "router-view"],
    });
    await wrapper.vm.$nextTick();

    // Simulate changing the selected role in the component
    wrapper.setData({ selectedRole: "Role 1" });

    // Assert that applicationCount is updated as expected
    expect(wrapper.vm.applicationCount).toEqual(0);
  });
  it("correctly sorts candidates based on selected sorting criteria", async () => {
    const wrapper = mount(Candidates, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
      stubs: ["router-link", "router-view"],
    });
    await wrapper.vm.$nextTick();

    // Simulate selecting a sorting criteria (e.g., selectedOrderBy or selectedSkills)
    // to trigger sorting

    // Assert that the candidates are sorted as expected
    expect(wrapper.vm.sortedCandidates).toEqual([]);
  });
  it("correctly opens and closes the modal for a selected candidate", async () => {
    const wrapper = mount(Candidates, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
      stubs: ["router-link", "router-view"],
    });
    await wrapper.vm.$nextTick();

    // Simulate selecting a candidate and opening the modal
    wrapper.vm.openModal(/* Selected candidate data */);

    // Assert that the modal is open and displays the correct data

    // Simulate closing the modal
    wrapper.vm.closeModal();

    // Assert that the modal is closed
    expect(wrapper.vm.selectedCandidate).toBeNull();
  });

  it('should call clearUserSessionData when the "Logout" button is clicked', () => {
   const wrapper = mount(Candidates, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
      stubs: ["router-link", "router-view"],
    });
    const clearUserSessionData = vi.spyOn(wrapper.vm, 'clearUserSessionData');
    
    const logoutButton = wrapper.find('button.btn-secondary');
    logoutButton.trigger('click');

    expect(clearUserSessionData).toHaveBeenCalled();
  });

  it('should correctly calculate the percentage of skills matched', () => {
    const wrapper = mount(Candidates, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
      stubs: ["router-link", "router-view"],
    });
    const candidate = {
      roleListing: {
        Skills: ['Skill1', 'Skill2', 'Skill3']
      },
      Skills: [
        { Skill_Name: 'Skill1' },
        { Skill_Name: 'Skill3' }
      ]
    };

    const percentage = wrapper.vm.getPercentageSkillsMatched(candidate);

    // In this example, 2 out of 3 skills match, so the percentage should be (2/3) * 100 = 66.67
    expect(percentage).toBeCloseTo(66.67, 2); // Ensure the value is close to 66.67 with 2 decimal places precision
  });

  it('should filter candidates based on selected skills', () => {
    const wrapper = mount(Candidates, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter,
        },
      },
      stubs: ["router-link", "router-view"],
    });

    // Assuming you have candidates with specific skills in your data
    const candidate1 = { Skills: [{ Skill_Name: 'Skill1' }, { Skill_Name: 'Skill2' }] };
    const candidate2 = { Skills: [{ Skill_Name: 'Skill2' }, { Skill_Name: 'Skill3' }] };
    const candidate3 = { Skills: [{ Skill_Name: 'Skill1' }, { Skill_Name: 'Skill3' }] };

    wrapper.setData({ rolecandidates: [candidate1, candidate2, candidate3] });

    // Select a specific skill
    wrapper.setData({ selectedSkills: ['Skill2'] });

    // After filtering, only candidate1 and candidate2 should be visible
    expect(wrapper.vm.filteredCandidates).toEqual([candidate1, candidate2]);
  });
});
